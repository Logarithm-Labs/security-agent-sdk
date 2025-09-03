import threading
import time
from abc import ABCMeta, abstractmethod
from collections import deque
from typing import Optional

from dotenv import load_dotenv
from virtuals_acp import ACPJob, ACPJobPhase, ACPMemo, IDeliverable, VirtualsACP
from virtuals_acp.env import EnvSettings

from security_agent_sdk.models.input import RequirementScheme
from security_agent_sdk.models.output import AuditResult, VulnerabilityCount

load_dotenv(override=True)


class SecurityAgent(metaclass=ABCMeta):
    """
    Abstract base class for security agents.

    Defines a unified interface for performing audits.
    """

    @abstractmethod
    def process_request(self, requirement: RequirementScheme) -> AuditResult:
        """
        Perform an audit based on the provided requirements.

        Args:
            requirement: Scheme with data for audit (contracts, repository, etc.).

        Returns:
            Audit results in standardized `AuditResult` format.
        """
        pass


class MockSecurityAgent(SecurityAgent):
    """
    Test auditor that returns hardcoded data.

    Does not perform real network requests.
    """

    def process_request(self, requirement: RequirementScheme) -> AuditResult:
        audited_contracts = len(requirement.contracts)
        return AuditResult(
            audited_files=1,
            audited_contracts=audited_contracts,
            vulnerability_count=VulnerabilityCount(high=1, medium=2, low=3),
            total_lines=150,
            security_score=85.5,
        )


def seller(use_thread_lock: bool = True):
    env = EnvSettings()

    if env.WHITELISTED_WALLET_PRIVATE_KEY is None:
        raise ValueError("WHITELISTED_WALLET_PRIVATE_KEY is not set")
    if env.SELLER_AGENT_WALLET_ADDRESS is None:
        raise ValueError("SELLER_AGENT_WALLET_ADDRESS is not set")
    if env.SELLER_ENTITY_ID is None:
        raise ValueError("SELLER_ENTITY_ID is not set")

    try:
        security_agent: SecurityAgent = MockSecurityAgent()
        print("Mock Security Agent initialized.")
    except Exception as e:
        print(f"Failed to initialize security agent: {e}")
        return

    job_queue = deque()
    job_queue_lock = threading.Lock()
    job_event = threading.Event()

    def safe_append_job(job, memo_to_sign: Optional[ACPMemo] = None):
        if use_thread_lock:
            with job_queue_lock:
                job_queue.append((job, memo_to_sign))
        else:
            job_queue.append((job, memo_to_sign))

    def safe_pop_job():
        if use_thread_lock:
            with job_queue_lock:
                if job_queue:
                    return job_queue.popleft()
        else:
            if job_queue:
                return job_queue.popleft()
        return None, None

    def job_worker():
        while True:
            job_event.wait()
            while True:
                job, memo_to_sign = safe_pop_job()
                if not job:
                    break
                threading.Thread(
                    target=handle_job_with_delay, args=(job, memo_to_sign), daemon=True
                ).start()
            if use_thread_lock:
                with job_queue_lock:
                    if not job_queue:
                        job_event.clear()
            else:
                if not job_queue:
                    job_event.clear()

    def handle_job_with_delay(job, memo_to_sign):
        try:
            process_job(job, memo_to_sign)
            time.sleep(1.5)
        except Exception as e:
            print(f"✖ Error processing job {getattr(job, 'id', '?')}: {e}")

    def on_new_task(job: ACPJob, memo_to_sign: Optional[ACPMemo] = None):
        print(f"[on_new_task] job {job.id} phase={job.phase}")
        safe_append_job(job, memo_to_sign)
        job_event.set()

    def process_job(job: ACPJob, memo_to_sign: Optional[ACPMemo] = None):
        if (
            job.phase == ACPJobPhase.REQUEST
            and memo_to_sign is not None
            and memo_to_sign.next_phase == ACPJobPhase.NEGOTIATION
        ):
            print(f"[process_job] responding accept for job {job.id}")
            job.respond(True)
            return

        if (
            job.phase == ACPJobPhase.TRANSACTION
            and memo_to_sign is not None
            and memo_to_sign.next_phase == ACPJobPhase.EVALUATION
        ):
            requirement_data = job.service_requirement

            if requirement_data is None:
                print(
                    f"✖ Error: service_requirement for job {job.id} does not contain 'data' field."
                )
                return

            try:
                requirement = RequirementScheme.model_validate(requirement_data)
            except Exception as e:
                print(f"✖ Error parsing requirement for job {job.id}: {e}")
                return

            final_result = security_agent.process_request(requirement).model_dump_json()

            deliverable = IDeliverable(type="json", value=final_result)
            job.deliver(deliverable)
            return

        if job.phase == ACPJobPhase.COMPLETED:
            print(f"[process_job] completed job {job.id}")
            return

        if job.phase == ACPJobPhase.REJECTED:
            print(f"[process_job] rejected job {job.id}")
            return

        print(f"[process_job] noop for job {job.id} at phase {job.phase}")

    threading.Thread(target=job_worker, daemon=True).start()

    VirtualsACP(
        wallet_private_key=env.WHITELISTED_WALLET_PRIVATE_KEY,
        agent_wallet_address=env.SELLER_AGENT_WALLET_ADDRESS,
        on_new_task=on_new_task,
        entity_id=env.SELLER_ENTITY_ID,
    )

    print("Seller is listening for new tasks...")
    threading.Event().wait()


if __name__ == "__main__":
    seller()
