import pytest
from app.services.smart_scheduler import smart_scheduler
from app.services.spam_checker import spam_checker

def test_smart_scheduler_country_and_timezone_detection():
    # 1. Stanford (US Pacific)
    res_stanford = smart_scheduler.detect_timezone("prof@cs.stanford.edu")
    assert res_stanford["country"] == "United States"
    assert res_stanford["timezone"] == "America/Los_Angeles"

    # 2. Oxford (UK)
    res_oxford = smart_scheduler.detect_timezone("dr.john@ox.ac.uk")
    assert res_oxford["country"] == "United Kingdom"
    assert res_oxford["timezone"] == "Europe/London"

    # 3. ETH Zurich (Switzerland)
    res_eth = smart_scheduler.detect_timezone("faculty@ethz.ch")
    assert res_eth["country"] == "Switzerland"
    assert res_eth["timezone"] == "Europe/Zurich"

    # 4. TUM Munich (Germany)
    res_tum = smart_scheduler.detect_timezone("weber@tum.de")
    assert res_tum["country"] == "Germany"
    assert res_tum["timezone"] == "Europe/Berlin"

    # 5. NUS (Singapore)
    res_nus = smart_scheduler.detect_timezone("advisor@nus.edu.sg")
    assert res_nus["country"] == "Singapore"
    assert res_nus["timezone"] == "Asia/Singapore"

def test_smart_scheduler_friday_and_weekend_protection():
    schedule = smart_scheduler.calculate_optimal_schedule("faculty@cs.berkeley.edu")
    
    assert schedule["friday_protected"] is True
    assert "optimal_slot_local" in schedule
    assert "optimal_slot_ist" in schedule
    assert "diff_hours_str" in schedule
    assert "activity_state" in schedule
    
    # Verify Friday is NEVER scheduled
    assert "Friday" not in schedule["optimal_slot_local"]
    assert "Saturday" not in schedule["optimal_slot_local"]
    assert "Sunday" not in schedule["optimal_slot_local"]

def test_spam_checker_catches_spam_triggers():
    spammy_subject = "URGENT 100% SCHOLARSHIP REQUEST!!!"
    spammy_body = """
    Respected Sir,
    I beg to state that I need 100% scholarship and free funding for PhD.
    Kindly revert back immediately. Give me a chance at your prestigious university.
    Here is my CV: http://bit.ly/my-phd-cv
    """
    analysis = spam_checker.analyze(
        subject=spammy_subject,
        body=spammy_body,
        recipient_name="Andrew Ng"
    )

    assert analysis["deliverability_score"] < 50
    assert analysis["is_safe_to_send"] is False
    assert any("Respected Sir" in flag or "greeting" in flag.lower() for flag in analysis["flags"])
    assert any("bit.ly" in flag for flag in analysis["flags"])
    assert len(analysis["suggestions"]) > 0

def test_spam_checker_approves_grounded_academic_email():
    clean_subject = "Prospective PhD Inquiry - Distributed Consensus Systems - Sumit Raj"
    clean_body = """Dear Professor Stonebreaker,

I hope you are having a productive week.

My name is Sumit Raj, and I hold a Master's degree in Computer Science specializing in Distributed Systems. I have followed your laboratory's recent publications with great enthusiasm, particularly your recent paper on Byzantine Fault Tolerant consensus architectures. Your methodology regarding low-latency replication strongly aligns with my previous thesis work on distributed state machine replication.

I am writing to inquire if you are considering new PhD students for your research group for the upcoming intake. I have attached my CV and would welcome the opportunity to discuss your ongoing laboratory projects or answer any questions about my technical background.

Would you be open to a brief 15-minute introductory call at your convenience?

Thank you for your time and consideration.

Sincerely,
Sumit Raj
raj@alumni.edu
"""
    analysis = spam_checker.analyze(
        subject=clean_subject,
        body=clean_body,
        recipient_name="Michael Stonebreaker"
    )

    assert analysis["deliverability_score"] >= 80
    assert analysis["is_safe_to_send"] is True
    assert analysis["rating"] in ["EXCELLENT", "GOOD"]
    assert len(analysis["positive_signals"]) >= 3
