import sys
import emoji
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel

class EmojiSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Emoji Search by Description")
        self.setGeometry(100, 100, 600, 400)

        self.filtered_emojis = []
        self.selected_index = 0

        # Set up the layout
        self.layout = QVBoxLayout()

        # Create a search input field
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search for an emoji description...")
        self.search_input.textChanged.connect(self.search_emojis)
        self.layout.addWidget(self.search_input)

        # Label to display the filtered emojis
        self.emoji_display = QLabel("No emojis found!", self)
        self.emoji_display.setWordWrap(True)
        self.layout.addWidget(self.emoji_display)

        # Label to display the selected emoji
        self.selected_emoji_label = QLabel("Selected Emoji: None", self)
        self.layout.addWidget(self.selected_emoji_label)

        # Set up the layout for the QWidget
        self.setLayout(self.layout)

    def search_emojis(self):
        search_query = self.search_input.text().lower()  # Get the search query from the input field
        self.filtered_emojis.clear()

        # Filter emojis based on the description
        for emo_char, emo_desc in emoji.EMOJI_DATA.items():
            if (search_query in emo_desc["en"].lower()):
                self.filtered_emojis.append(emo_char)

        self.update_emoji_display()

    def update_emoji_display(self):
        if self.filtered_emojis:
            # Join the emojis with space and update the label
            self.emoji_display.setText(" ".join(self.filtered_emojis))
        else:
            self.emoji_display.setText("No emojis found!")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            # Navigate up
            self.selected_index = (self.selected_index - 1) % len(self.filtered_emojis) if self.filtered_emojis else 0
            self.update_emoji_display_highlighted()
        elif event.key() == Qt.Key_Down:
            # Navigate down
            self.selected_index = (self.selected_index + 1) % len(self.filtered_emojis) if self.filtered_emojis else 0
            self.update_emoji_display_highlighted()
        elif event.key() == Qt.Key_Return:
            # Select the emoji on Enter
            self.select_emoji()

    def update_emoji_display_highlighted(self):
        highlighted_emojis = []
        for i, emoji in enumerate(self.filtered_emojis):
            if i == self.selected_index:
                highlighted_emojis.append(f"[{emoji}]")  # Highlight the selected emoji
            else:
                highlighted_emojis.append(emoji)

        self.emoji_display.setText(" ".join(highlighted_emojis) if self.filtered_emojis else "No emojis found!")

    def select_emoji(self):
        if self.filtered_emojis:
            selected_emoji = self.filtered_emojis[self.selected_index]
            self.selected_emoji_label.setText(f"Selected Emoji: {selected_emoji}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmojiSearchApp()
    window.show()
    sys.exit(app.exec_())
