from portfolio_lab.demo import main as demo_main
from portfolio_lab.report import main as report_main


def test_demo_prints_the_hand_worked_variance(capsys):
    demo_main()
    output = capsys.readouterr().out
    assert "0.006972" in output
    assert "Component risk" in output


def test_report_prints_sample_stats_and_strategies(capsys):
    report_main(["--market", "UK", "--window", "1y", "--tickers", "AZN.L,SHEL.L,IGLT.L"])
    output = capsys.readouterr().out
    assert "AZN.L" in output
    assert "n/a" in output
    assert "Cautious" in output
    assert "Balanced" in output
