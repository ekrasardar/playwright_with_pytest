import pytest
from pytest_testrail.plugin import pytestrail


class SearchTest:
    @pytest.mark.search
    @pytestrail.case('please_insert_testrail_case_id_here')
    @pytest.mark.skip_for_prod  #use this line in case to ignore this test in prod
    def test_search(self, driver) -> None:
        driver.home.google_search_by_name("playwright")
