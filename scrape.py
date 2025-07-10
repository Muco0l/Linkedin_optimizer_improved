#---impoerting necessary libraries
from apify_client import ApifyClient
import streamlit as st
#---setting up Apify API key
APIFY_API_KEY_ = st.secrets["APIFY_API_KEY"]
def get_profile(linkedin_url):
    try:
        client = ApifyClient(APIFY_API_KEY_)
        run_input = { "profileUrls": [linkedin_url] }
        run = client.actor("2SyF0bVxmgGr8IVCZ").call(run_input=run_input)
        for profile in client.dataset(run["defaultDatasetId"]).iterate_items():
            summary_parts = []

            summary_parts.append(f"Name: {profile.get('fullName')}")
            summary_parts.append(f"Headline: {profile.get('headline')}")
            summary_parts.append(f"About: {profile.get('about', '—')}")
            summary_parts.append(f"Connections: {profile.get('connections', '—')}")
            summary_parts.append(f"Followers: {profile.get('followers', '—')}")
            summary_parts.append(f"Country: {profile.get('addressCountryOnly', '—')}")
            summary_parts.append(f"CurrentEmploymentSize: {profile.get('companySize', '—')}")
            skills = profile.get("skills", [])
            summary_parts.append("Skills:")
            if skills:
                for skill in skills:
                    summary_parts.append(f"   - {skill}")
            else:
                summary_parts.append("   - —")

            experiences = profile.get("experiences", [])
            summary_parts.append(" Experience:")
            if experiences:
                for exp in experiences:
                    summary_parts.append(f"   - {exp.get('title')} at {exp.get('subtitle')} ({exp.get('caption')})")
            else:
                summary_parts.append("   - No experience listed.")

            educations = profile.get("educations", [])
            summary_parts.append("Education:")
            if educations:
                for edu in educations:
                    summary_parts.append(f"   - {edu.get('title')} ({edu.get('caption', '')})")
            else:
                summary_parts.append("   - No education listed.")
            print("Profile fetched successfully.")
            print("\n".join(summary_parts))
            return "\n".join(summary_parts)
        return "Error: No profile data found"
    except Exception as e:
        return f"Error: {str(e)}"