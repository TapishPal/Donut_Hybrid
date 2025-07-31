
import streamlit as st
import requests
import json
import base64 # Import base64 for image display, although Streamlit handles this usually

# --- UI Configuration ---
st.set_page_config(
    page_title="Invoice OCR with Donut",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("📄 Invoice Data Extractor (Donut DocVQA)")
st.markdown("Upload an invoice image and get key information extracted automatically.")

# --- Backend API Endpoint ---
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000"

# --- UI Elements ---
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

# Placeholders for dynamic content to ensure consistent layout
image_placeholder = st.empty()
loading_placeholder = st.empty()
error_placeholder = st.empty()
results_placeholder = st.empty()

# Add a session state variable to control button visibility and prevent re-runs
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Button to trigger processing
process_button_clicked = st.button("Process Invoice", disabled=uploaded_file is None)

if uploaded_file is not None:
    # Display the uploaded image
    with image_placeholder.container():
        st.image(
            uploaded_file, 
            caption='Uploaded Image', 
            width=400
        )

    # If a new file is uploaded or button is clicked, reset processed state
    if process_button_clicked:
        st.session_state.processed = True
    elif not st.session_state.processed: # Only clear if not processing and no new click
        loading_placeholder.empty()
        error_placeholder.empty()
        results_placeholder.empty()


if st.session_state.processed and uploaded_file is not None:
    loading_placeholder.info("Processing image... This may take a moment.")
    error_placeholder.empty() # Clear previous errors
    results_placeholder.empty() # Clear previous results

    # Prepare the file for sending
    # `uploaded_file.getvalue()` returns bytes
    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

    try:
        # Make the POST request to your FastAPI backend
        response = requests.post(f"{FASTAPI_BACKEND_URL}/process_invoice", files=files)

        if response.status_code == 200:
            results = response.json()
            loading_placeholder.empty() # Clear loading message
            results_placeholder.success("OCR completed successfully!")

            # Display extracted results
            with results_placeholder.container(): # Use a container to group results
                st.subheader("Extracted Invoice Data:")
                if results:
                    # Create a grid for better display, max 2 columns for smaller screens
                    cols = st.columns(2)
                    col_idx = 0
                    for field, value in results.items():
                        with cols[col_idx]:
                            st.markdown(f"**{field.replace('_', ' ').upper()}:**")
                            # The backend's clean_generated_text (if fixed) should return a string.
                            # The check for list is a fallback if utils.py is still returning a list.
                            display_value = " ".join(value) if isinstance(value, list) else value
                            st.code(display_value, language='text')
                        col_idx = (col_idx + 1) % len(cols)
                else:
                    st.write("No specific data fields extracted. Check the image quality or backend configuration.")

            # Option to download raw JSON
            st.download_button(
                label="Download Raw JSON",
                data=json.dumps(results, indent=2),
                file_name=f"{uploaded_file.name.split('.')[0]}_extracted_data.json",
                mime="application/json"
            )

        elif response.status_code == 400:
            loading_placeholder.empty()
            error_placeholder.error(f"Error 400: Bad Request. Details: {response.json().get('detail', 'The file might be invalid or something else went wrong.')}")
        else: # Handle other HTTP errors (e.g., 500 from backend)
            loading_placeholder.empty()
            error_details = response.json().get('detail', 'Unknown error.')
            error_placeholder.error(f"Backend Error {response.status_code}: {error_details}")

    except requests.exceptions.ConnectionError:
        loading_placeholder.empty()
        error_placeholder.error(f"Could not connect to the backend server at {FASTAPI_BACKEND_URL}. Please ensure the backend is running and accessible.")
    except json.JSONDecodeError:
        loading_placeholder.empty()
        error_placeholder.error("Failed to decode JSON response from backend. The backend might have returned an invalid response.")
    except Exception as e:
        loading_placeholder.empty()
        error_placeholder.error(f"An unexpected error occurred: {e}")
    finally:
        # Reset processed state after attempt, whether successful or not,
        # so the button can be clicked again or new file can be chosen.
        st.session_state.processed = False

st.markdown("---")
st.caption("Powered by Donut DocVQA and FastAPI.")