import requests
import json
import argparse
import os


def test_tool(method, params={}):
    """
    Test FMP tool

    Args:
        method: The tool method name
        params: Request parameters (optional)
    """

    print(f"\nTesting tool: {method}")
    print(f"Parameters: {params}")

    try:
        headers = {"Content-Type": "application/json"}
        data = params
        url = f"http://localhost:30010/call_tool/{method}"
        response = requests.post(url, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("status") is True:
                    print("✅ Test successful")
                    print(
                        f"Response data: {json.dumps(result.get('result'), indent=2, ensure_ascii=False)[:500]}..."
                    )
                else:
                    print(
                        f"⚠️ Request successful but returned a failed status: {result.get('result')}"
                    )
            except json.JSONDecodeError:
                print(f"⚠️ Response is not valid JSON format: {response.text[:200]}")
        else:
            print(f"❌ Request failed: HTTP {response.status_code}")
            print(f"Response content: {response.text[:200]}")

    except Exception as e:
        print(f"❌ An error occurred during the test: {str(e)}")


def main(test_cases):
    if test_cases is None:
        print("Error, test_cases is None!")
        return

    print("Starting FMP tool test...")
    print("=" * 50)

    for test_case in test_cases:
        method = test_case.get("name", None)
        params = test_case.get("params", None)

        if method is None:
            print("Error, the method is None")

        if params is None:
            print("Error, params is None!")

        test_tool(method, params)
        print("=" * 50)

    print("\nTest complete!")


def get_file_path(domain_name: str) -> str:
    # ! switch to your own file path
    base_file_path = "/data/xiyuanyang/Agent/tool_backends/MCP/server/ProbeCode/CodingAgent/llm/tools/test"
    file_path = os.path.join(base_file_path, f"{domain_name.strip()}.json")
    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Several test config for testing MCP server."
    )
    parser.add_argument("--config_name", nargs="+", default=None)
    args = parser.parse_args()

    configs = args.config_name

    for config in configs:
        config_path = get_file_path(config)
        print(f"Running {config} domain in path: {config_path}")
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            main(test_cases=config_data)
