import pytest, pytest_bdd, time
from conftest import context
from pytest_bdd import scenario, scenarios, given, when, then, parsers
#===============================================
# scenarios('') # pytest.ini: bdd_features_base_dir
# scenarios('test_fullScenario.feature')
scenarios('test_example.feature')
#===============================================
@then('return failed')
def step_impl():
    assert False, 'assert "Failed"'

@then('return passed')
def step_impl():
    pass

@then(parsers.parse('return "{result}"'))
def step_impl(result):
    if result.lower() in 'passed':
        pass
    elif result.lower() in 'failed':
        assert False, 'assert "Failed"'