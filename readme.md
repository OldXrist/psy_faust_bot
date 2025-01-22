# Telegram Bot: Personal Psychological Assistant

## Overview
This Telegram bot is a personal psychological assistant designed to help users create, edit, and refine textual content related to psychological topics. It leverages Groq's API for natural language understanding and speech-to-text functionality, making it a versatile tool for psychologists and individuals seeking assistance in generating or editing psychological content.

---

## Features

### Core Functionalities:
- **Text Generation**: Create content on psychological topics.
- **Text Editing**: Refine and enhance existing text, including grammar and tone corrections.
- **Speech-to-Text**: Prompt Groq API via voice messages using speech recognition model.
- **Rate Limit Awareness**: Notify users when OpenAI API limits are reached and provide updates when the limit resets.
- **Access Control**: Restrict bot usage to authorized users based on their Telegram user IDs.

---

### Prerequisites
- Python 3.11+
- Poetry (for dependency management)
- FFmpeg (for speech-to-text functionality)
- Docker (optional, for containerized deployment)
