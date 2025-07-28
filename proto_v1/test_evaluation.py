# test_evaluation.py
import requests
import time
import json
import pandas as pd
import os

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:5000/reconcile"
RESULTS_DIR = "evaluation_results"
RESPONSE_TIMES_FILE = os.path.join(RESULTS_DIR, "response_times.csv")
MATCH_ACCURACY_FILE = os.path.join(RESULTS_DIR, "match_accuracy.csv")

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Test Cases ---
# This list defines the queries to send and their expected outcomes.
# Each dictionary represents a test scenario.
TEST_CASES =, # Expecting multiple, order might vary
        "expected_score_min": 0.8,
        "expected_match_type": "partial_substring_match"
    },
    {
        "case": "Case Insensitivity",
        "query": "the hobbit", # Lowercase query
        "expected_id": "w008",
        "expected_score_min": 1.0,
        "expected_match_type": "exact_match"
    },
    {
        "case": "No Match Found",
        "query": "NonExistentBook",
        "expected_id": None, # Expecting no match
        "expected_score_min": 0.0,
        "expected_match_type": None
    },
    {
        "case": "Error - Missing Query Parameter",
        "query": None, # Explicitly omit query parameter
        "endpoint": API_BASE_URL, # Use the reconcile endpoint
        "expected_status_code": 400,
        "expected_error_message_part": "Missing 'query' parameter",
        "is_error_case": True
    },
    {
        "case": "Query with Trailing Spaces",
        "query": "  George Orwell  ",
        "expected_id": "a001",
        "expected_score_min": 1.0,
        "expected_match_type": "exact_match"
    },
    {
        "case": "Partial Match - Author Name",
        "query": "fitzgerald",
        "expected_id": "a002",
        "expected_score_min": 0.8,
        "expected_match_type": "partial_substring_match"
    }
]

# --- Evaluation Function ---
def run_evaluation():
    """
    Executes the test cases, sends requests to the API, and collects evaluation data.
    Stores response times and match accuracy results in CSV files.
    """
    response_times_data =
    match_accuracy_data =

    print(f"Starting evaluation with {len(TEST_CASES)} test cases...")
    print("-" * 50)

    for i, test_case in enumerate(TEST_CASES):
        query = test_case.get("query")
        case_description = test_case.get("case", f"Test Case {i+1}")
        is_error_case = test_case.get("is_error_case", False)
        endpoint = test_case.get("endpoint", API_BASE_URL) # Use specific endpoint if provided

        print(f"Running: {case_description} (Query: '{query}')")

        start_time = time.perf_counter()
        try:
            if is_error_case and query is None and endpoint == API_BASE_URL:
                # Specific case for missing query param on /reconcile
                response = requests.get(endpoint)
            elif endpoint!= API_BASE_URL:
                # For testing other endpoints like home
                response = requests.get(endpoint)
            else:
                # Standard reconciliation query
                response = requests.get(API_BASE_URL, params={"query": query})
            
            response_time = (time.perf_counter() - start_time) * 1000 # in milliseconds
            
            # Record response time
            response_times_data.append({
                "case": case_description,
                "query": query,
                "response_time_ms": response_time,
                "status_code": response.status_code
            })

            if is_error_case:
                # Validate error response or non-JSON response (like home page)
                actual_status_code = response.status_code
                expected_status_code = test_case.get("expected_status_code")
                
                test_passed = (actual_status_code == expected_status_code)
                notes = f"Status code mismatch: Expected {expected_status_code}, Got {actual_status_code}"

                if "expected_error_message_part" in test_case:
                    try:
                        actual_error_message = response.json().get("error", "")
                        expected_error_message_part = test_case.get("expected_error_message_part")
                        if expected_error_message_part in actual_error_message:
                            test_passed = test_passed and True
                            notes = "Error message part found"
                        else:
                            test_passed = False
                            notes += f"; Error message mismatch: Expected '{expected_error_message_part}', Got '{actual_error_message}'"
                    except json.JSONDecodeError:
                        test_passed = False
                        notes = "Expected JSON error, but response was not JSON"
                elif "expected_response_text_part" in test_case:
                    actual_text = response.text
                    expected_text_part = test_case.get("expected_response_text_part")
                    if expected_text_part in actual_text:
                        test_passed = test_passed and True
                        notes = "Expected text part found"
                    else:
                        test_passed = False
                        notes += f"; Response text mismatch: Expected '{expected_text_part}', Got '{actual_text[:50]}...'"

                match_accuracy_data.append({
                    "case": case_description,
                    "query": query,
                    "expected_outcome": f"Status {expected_status_code}",
                    "actual_outcome": f"Status {actual_status_code}",
                    "passed": test_passed,
                    "notes": notes
                })
            else:
                # Validate successful reconciliation response
                actual_results = response.json()
                expected_id = test_case.get("expected_id")
                expected_ids = test_case.get("expected_ids") # For multiple expected matches
                expected_score_min = test_case.get("expected_score_min")
                expected_match_type = test_case.get("expected_match_type")

                passed = False
                notes = "No expected match found in results"
                actual_top_match_id = None
                actual_top_match_score = None
                actual_top_match_type = None

                if expected_id is None and expected_ids is None: # Expecting no match
                    passed = (len(actual_results) == 0)
                    notes = "Expected no match, received empty list" if passed else f"Expected no match, received {len(actual_results)} results"
                elif expected_id is not None: # Expecting a single specific top match
                    if actual_results:
                        top_result = actual_results # Assume top result is the most relevant
                        actual_top_match_id = top_result.get("id")
                        actual_top_match_score = top_result.get("score")
                        actual_top_match_type = top_result.get("match_type")

                        if (actual_top_match_id == expected_id and
                            actual_top_match_score >= expected_score_min and
                            actual_top_match_type == expected_match_type):
                            passed = True
                            notes = "Top result matches expectation"
                        else:
                            notes = f"Top result mismatch: Expected ID {expected_id}, Got {actual_top_match_id}"
                            if any(res.get("id") == expected_id for res in actual_results):
                                notes += " (Expected ID found, but not as top result or criteria not met)"
                            else:
                                notes += " (Expected ID not found in any results)"
                    else:
                        notes = "Expected match, but received empty results"
                elif expected_ids is not None: # Expecting multiple specific matches
                    # Check if all expected IDs are present in the actual results
                    actual_ids = {res.get("id") for res in actual_results}
                    all_expected_ids_present = all(eid in actual_ids for eid in expected_ids)
                    
                    # Check if all actual results meet the score/type criteria
                    all_actual_results_valid = True
                    for res in actual_results:
                        if not (res.get("score") >= expected_score_min and res.get("match_type") == expected_match_type):
                            all_actual_results_valid = False
                            break
                    
                    passed = all_expected_ids_present and all_actual_results_valid and (len(actual_results) == len(expected_ids))
                    notes = "All expected IDs found and criteria met" if passed else "Mismatch in expected IDs or criteria"


                match_accuracy_data.append({
                    "case": case_description,
                    "query": query,
                    "expected_id": expected_id if expected_id is not None else str(expected_ids),
                    "expected_score_min": expected_score_min,
                    "expected_match_type": expected_match_type,
                    "actual_top_match_id": actual_top_match_id,
                    "actual_top_match_score": actual_top_match_score,
                    "actual_top_match_type": actual_top_match_type,
                    "passed": passed,
                    "notes": notes
                })

        except requests.exceptions.ConnectionError:
            print(f"  ERROR: Could not connect to API. Is Flask app running at {endpoint.split('/reconcile')}?")
            response_times_data.append({
                "case": case_description,
                "query": query,
                "response_time_ms": None,
                "status_code": "Connection Error"
            })
            match_accuracy_data.append({
                "case": case_description,
                "query": query,
                "expected_outcome": "API reachable",
                "actual_outcome": "Connection Error",
                "passed": False,
                "notes": "API not reachable"
            })
        except json.JSONDecodeError:
            print(f"  ERROR: Could not decode JSON response for query '{query}'. Response: {response.text[:100]}...")
            match_accuracy_data.append({
                "case": case_description,
                "query": query,
                "expected_outcome": "Valid JSON",
                "actual_outcome": "JSON Decode Error",
                "passed": False,
                "notes": "Invalid JSON response"
            })
        except Exception as e:
            print(f"  An unexpected error occurred during testing for query '{query}': {e}")
            match_accuracy_data.append({
                "case": case_description,
                "query": query,
                "expected_outcome": "No unexpected error",
                "actual_outcome": f"Unexpected Error: {e}",
                "passed": False,
                "notes": "Unhandled exception during test"
            })
        print("-" * 50)

    # Save results to CSV
    pd.DataFrame(response_times_data).to_csv(RESPONSE_TIMES_FILE, index=False)
    pd.DataFrame(match_accuracy_data).to_csv(MATCH_ACCURACY_FILE, index=False)

    print("\nEvaluation complete. Results saved to:")
    print(f"- {RESPONSE_TIMES_FILE}")
    print(f"- {MATCH_ACCURACY_FILE}")

if __name__ == "__main__":
    run_evaluation()