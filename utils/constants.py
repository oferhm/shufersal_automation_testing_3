# utils/constants.py
# ──────────────────────────────────────────────────────────────────────────────
# Constants — Single source of truth for URLs, selectors, and test data.
#
# WHY: Never hard-code strings inside test methods or page objects.
#      One change here fixes the entire suite instantly.
# ──────────────────────────────────────────────────────────────────────────────


class URLs:
    HOME = "https://www.shufersal.co.il/online/"


class SearchData:
    MILK_KEYWORD = "חלב"          # Hebrew for "milk" — searched and verified throughout


class ExpectedText:
    LOGIN_HEADER = "התחברות"      # Hebrew for "login" — expected on the login redirect page


class Timeouts:
    DEFAULT    = 8_000            # ms — general element waits
    NAVIGATION = 15_000           # ms — full page load / redirect waits
    CART       = 10_000           # ms — cart panel open / item appear
