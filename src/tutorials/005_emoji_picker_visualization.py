from fasthtml.common import *
from src.page_utils import TutorialPage, create_form

# Custom component for the emoji picker
def EmojiPicker():
    return Div(
        NotStr('<emoji-picker></emoji-picker>'),
        NotStr('''
            <script type="module">
                import emojiPickerElement from "https://cdn.skypack.dev/emoji-picker-element";

                document.querySelector("emoji-picker").addEventListener("emoji-click", (event) => {
                    console.log(event.detail);
                    // Display the selected emoji on the page
                    const emojiDisplay = document.getElementById('emoji_display');
                    if (emojiDisplay) {
                        emojiDisplay.innerHTML = `You selected: ${event.detail.unicode}`; // Update the display area
                    }
                    // Store the selected emoji in hidden inputs for step 2
                    const selectedEmojiInput = document.getElementsByName('selected_emoji')[0];                    
                    
                    if (selectedEmojiInput) {
                        selectedEmojiInput.value = event.detail.unicode; // Set the value of the hidden input
                    } else {
                        console.error("Hidden input for selected emoji not found");
                    }

                });
            </script>
        ''')
    )


page = TutorialPage(
    page_number=5,
    display_name="Emoji Picker Visualization",
    slug="emoji-picker-visualization",
)

page_classes = "bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 w-full max-w-4xl mx-auto"

@page.step(1)
async def step_1(request, form_data=None):    
    return Div(
        H1("Emoji Picker", cls="text-2xl font-bold mb-4"),
        P("Select an emoji:", cls="mb-4"),
        EmojiPicker(),
        Div(id="emoji_display", cls="mt-4"),
        create_form(action="?step=2",                      
                    selected_emoji=("hidden", "Selected Emoji", False)),  
                    cls=page_classes,
                    id="emoji-form"
    )

@page.step(2)
async def step_2(request, form_data=None):
    if form_data and 'selected_emoji' in form_data:
        request.session['selected_emoji'] = form_data['selected_emoji']
    selected_emoji = request.session.get('selected_emoji', 'No emoji selected')    
    return Div(
        H1("Step 2: Selected Emoji", cls="text-2xl font-bold mb-4"),
        P(f"You selected: {selected_emoji}", cls="mb-4"),
        Button("Back to Step 1", hx_get="?step=1", hx_target="#content", cls="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded mt-4"),
        cls=page_classes
    )