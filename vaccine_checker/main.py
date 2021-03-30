import json
import os
import requests
import time


def send_nys_webhook(site):

    url = os.getenv("SLACK_WEBHOOK_URL")
    payload = {
        "text": f"HOLY CRAP!!! {site['providerName']} ({site['vaccineBrandFullName']}): {'Has appointments!'}\n Sign up at <{site.get('3rdPartyURL')}>"
    }
    requests.request("POST", url, data=json.dumps(payload))


def run_nys(session: requests.Session):

    SITE_NUMBERS = [
        1014,  # medgar evans
        1000,  # javitts
        1019,  # javitts
    ]

    url = "https://am-i-eligible.covid19vaccine.health.ny.gov/api/get-providers"

    payload = '{"applicationId":"5623918908782047275","address":"11218","miles":"100","dob":"06/04/1985"}'
    headers = {
        "authority": "am-i-eligible.covid19vaccine.health.ny.gov",
        "accept": "application/json, text/plain, */*",
        "token": "disabled",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://am-i-eligible.covid19vaccine.health.ny.gov",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://am-i-eligible.covid19vaccine.health.ny.gov/Public/providers",
        "accept-language": "en-US,en;q=0.9",
    }

    response = session.post(url, headers=headers, data=payload, timeout=1.0)
    resp_json = response.json()
    sites = [site for site in resp_json if site["providerId"] in SITE_NUMBERS]

    for site in sites:
        if site["availableAppointments"] == "AA":
            print(
                f"{site['providerName']} ({site['vaccineBrandFullName']}): {'Has appointments!'}"
            )
            print("SENDING WEBHOOK!")
            send_nys_webhook(site)
        else:
            print(
                f"{site['providerName']} ({site['vaccineBrandFullName']}): {'No Appointments'}"
            )


def run():
    s = requests.Session()
    num_secs = os.getenv("REFRESH_SECS", 5)
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    print("💉 💉 💉 Starting up! 💉 💉 💉")
    print(f"Refresh every {num_secs} seconds")
    if webhook_url:
        print(f"Slack webhook: {webhook_url}")
    while True:
        print("RUNNING!")
        try:
            # check the 3 NYC sites
            run_nys(session=s)
        except Exception as err:
            print(f"Something went wrong! {err}")
        print("WAITING!")
        time.sleep(5)


if __name__ == "__main__":
    run()
