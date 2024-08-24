import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyAdsTTHqPLfZexuLI5Wxrj85r6o9aADQfk'
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Language Translator")

    # User input for the text to translate
    user_input = st.text_area(
        "Please enter the text you want to translate:",
        height=200
    )

    # Select target language
    target_language = st.selectbox(
        "Select the target language:",
        ["French", "Spanish", "German", "Chinese", "Japanese", "Hindi", "Arabic"]
    )

    # Button to translate the text
    if st.button("Translate"):
        if user_input.strip():
            # Create a prompt for translating the text
            prompt = f"""
            Please translate the following text to {target_language}:

            "{user_input}"

            The translation should be accurate and preserve the original meaning.
            """

            try:
                # Use the Gemini generative model to translate the text
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                translation = response.text

                # Store the translated text in the session state to keep it persistent
                st.session_state.translated_text = translation
                st.session_state.copy_status = "Copy Translation to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't generate the translation. Please try again later.")
        else:
            st.warning("Please provide text to translate.")

    # Check if the translated text is in session state
    if 'translated_text' in st.session_state:
        st.subheader("Your Translated Text:")
        translation_text_area = st.text_area("Translation:", st.session_state.translated_text, height=400, key="translation_content")

        # Button to copy translation to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Translation to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var translationContent = document.querySelector('#translation_content');
                    var range = document.createRange();
                    range.selectNode(translationContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
