# Advanced test endpoint with batch processing and detailed reporting
import pandas as pd
import os
import requests
import json
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Environment Variables
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')

# Path names
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(os.path.dirname(file_path))
data_path = os.path.join(repo_root, 'data')


def read_csv_random_input_samples(n_samples: int = 5) -> pd.DataFrame:
    """Read random samples from CSV file"""
    df_future_unseen_examples = pd.read_csv(os.path.join(data_path, 'future_unseen_examples.csv'))
    df_random_unseen_examples = df_future_unseen_examples.sample(
        n=min(n_samples, len(df_future_unseen_examples)), 
        random_state=42
    )
    return df_random_unseen_examples


def predict_property_price(property_data: dict, sample_id: int = None) -> dict:
    """
    Send a POST request to the API endpoint with property data
    """
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=property_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        result['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
        result['sample_id'] = sample_id
        result['status'] = 'success'
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout",
            "sample_id": sample_id,
            "status": "error",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "Connection error - Is the API running?",
            "sample_id": sample_id,
            "status": "error",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Request failed: {str(e)}",
            "sample_id": sample_id,
            "status": "error",
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


def test_single_sample(row: pd.Series, sample_id: int) -> dict:
    """Test a single sample and return results"""
    property_data = row.to_dict()
    
    print(f"Testing Sample {sample_id}...")
    
    result = predict_property_price(property_data, sample_id)
    
    if result['status'] == 'success':
        print(f"✅ Sample {sample_id}: ${result.get('prediction', 'N/A'):,.2f}")
    else:
        print(f"❌ Sample {sample_id}: {result.get('error', 'Unknown error')}")
    
    return {
        "sample_id": sample_id,
        "input_data": property_data,
        "result": result
    }


def test_api_endpoint_sequential(n_samples: int = 5) -> List[Dict[str, Any]]:
    """
    Test the API endpoint sequentially (one by one)
    """
    print(f"Testing API endpoint sequentially with {n_samples} samples...")
    
    df_samples = read_csv_random_input_samples(n_samples)
    results = []
    
    for index, row in df_samples.iterrows():
        result = test_single_sample(row, index + 1)
        results.append(result)
    
    return results


def test_api_endpoint_parallel(n_samples: int = 5, max_workers: int = 3) -> List[Dict[str, Any]]:
    """
    Test the API endpoint in parallel for faster execution
    """
    print(f"Testing API endpoint in parallel with {n_samples} samples (max {max_workers} workers)...")
    
    df_samples = read_csv_random_input_samples(n_samples)
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_sample = {
            executor.submit(test_single_sample, row, index + 1): index + 1 
            for index, row in df_samples.iterrows()
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_sample):
            result = future.result()
            results.append(result)
    
    # Sort results by sample_id
    results.sort(key=lambda x: x['sample_id'])
    return results


def generate_test_report(results: List[Dict[str, Any]]) -> dict:
    """Generate a comprehensive test report"""
    total_samples = len(results)
    successful_predictions = sum(1 for r in results if r['result']['status'] == 'success')
    failed_predictions = total_samples - successful_predictions
    
    # Calculate response times
    response_times = [r['result']['response_time_ms'] for r in results if 'response_time_ms' in r['result']]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    # Get predictions
    predictions = [
        r['result']['prediction'] 
        for r in results 
        if r['result']['status'] == 'success' and 'prediction' in r['result']
    ]
    
    report = {
        "summary": {
            "total_samples": total_samples,
            "successful_predictions": successful_predictions,
            "failed_predictions": failed_predictions,
            "success_rate": round(successful_predictions / total_samples * 100, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "min_response_time_ms": min(response_times) if response_times else 0,
            "max_response_time_ms": max(response_times) if response_times else 0
        },
        "predictions": {
            "count": len(predictions),
            "min_price": min(predictions) if predictions else 0,
            "max_price": max(predictions) if predictions else 0,
            "avg_price": sum(predictions) / len(predictions) if predictions else 0
        },
        "errors": [
            {
                "sample_id": r['sample_id'],
                "error": r['result']['error']
            }
            for r in results 
            if r['result']['status'] == 'error'
        ]
    }
    
    return report


def print_test_report(report: dict):
    """Print a formatted test report"""
    print("\n" + "="*60)
    print("📊 API TEST REPORT")
    print("="*60)
    
    summary = report['summary']
    predictions = report['predictions']
    
    print(f"📈 SUMMARY:")
    print(f"   Total samples tested: {summary['total_samples']}")
    print(f"   Successful predictions: {summary['successful_predictions']}")
    print(f"   Failed predictions: {summary['failed_predictions']}")
    print(f"   Success rate: {summary['success_rate']}%")
    print(f"   Average response time: {summary['avg_response_time_ms']}ms")
    print(f"   Response time range: {summary['min_response_time_ms']}ms - {summary['max_response_time_ms']}ms")
    
    print(f"\n💰 PREDICTIONS:")
    print(f"   Number of predictions: {predictions['count']}")
    print(f"   Price range: ${predictions['min_price']:,.2f} - ${predictions['max_price']:,.2f}")
    print(f"   Average price: ${predictions['avg_price']:,.2f}")
    
    if report['errors']:
        print(f"\n❌ ERRORS:")
        for error in report['errors']:
            print(f"   Sample {error['sample_id']}: {error['error']}")
    
    print("="*60)


def save_results_to_file(results: List[Dict[str, Any]], filename: str = "test_results.json"):
    """Save test results to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results saved to {filename}")


def main():
    """Main function to run the tests"""
    print("🚀 Starting API Endpoint Tests...")
    
    # Test with 10 samples
    n_samples = 10
    
    # Choose testing method
    print("\nChoose testing method:")
    print("1. Sequential testing (one by one)")
    print("2. Parallel testing (faster)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        results = test_api_endpoint_parallel(n_samples, max_workers=3)
    else:
        results = test_api_endpoint_sequential(n_samples)
    
    # Generate and print report
    report = generate_test_report(results)
    print_test_report(report)
    
    # Save results
    save_results_to_file(results)
    
    print("\n✅ Testing completed!")


if __name__ == "__main__":
    main() 