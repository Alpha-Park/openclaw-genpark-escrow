# -*- coding: utf-8 -*-
"""
Example usage of OpenClawGenParkEscrow
Demonstrates milestone verification and multi-signature tranche disbursement.
"""

from client import OpenClawGenParkEscrow

def main():
    escrow = OpenClawGenParkEscrow()

    res = escrow.evaluate_escrow_settlement(
        escrow_id="ESCROW-AGENT-CONTRACT-881",
        total_escrow_amount_usd=25000.00,
        required_quorum_count=2,
        multisig_signatures=["SIG-BUYER-CLIENT", "SIG-ORACLE-CONSENSUS"]
    )

    print("================================================================")
    print("OpenClaw GenPark Escrow - Settlement Evaluation")
    print("================================================================\n")
    print(f"Escrow Contract ID   : {res['escrow_id']}")
    print(f"Total Contract Amount : ${res['total_contract_amount_usd']:,.2f}")
    print(f"Multisig Quorum Met   : {res['multisig_quorum_satisfied']} ({res['active_signatures_verified']}/{res['required_quorum_threshold']} signatures)")
    print(f"Released Tranche Funds: ${res['total_released_funds_usd']:,.2f}")
    print(f"Remaining Locked Funds: ${res['remaining_locked_funds_usd']:,.2f}")
    print(f"Contract Status       : {res['contract_state']}\n")
    print("Milestone Breakdown:")
    for m in res['milestone_breakdown']:
        print(f"  * Milestone #{m['milestone_index']}: {m['title']:<40} | ${m['allocation_usd']:>8,.2f} -> {m['status']}")

if __name__ == "__main__":
    main()
