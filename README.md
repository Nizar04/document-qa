# YouTube Video Summarizer

A powerful Streamlit web application that generates summaries of YouTube videos using OpenAI's GPT-3.5 model. The application supports multiple languages, customizable summary styles, and video metadata display.

![Video Summarizer Demo](images/logo.svg)

## Features

- 🎥 Direct YouTube video transcript extraction
- 🌐 Multi-language support for transcripts and summaries
- 🎨 Customizable summary styles:
  - Concise
  - Detailed
  - Bullet Points
  - Academic
- 📏 Adjustable summary lengths
- 📊 Video metadata display (title, channel, thumbnail)
- 🔍 Language detection
- 💻 Clean and intuitive user interface

## Installation

1. Clone the repository:
```bash
git https://github.com/Nizar04/document-qa.git
cd document-qa
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenAI API key (optional):
```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Enter your OpenAI API key (if not set in `.env`)

4. Paste a YouTube URL and customize your summary preferences

5. Click "Generate Summary" to get your video summary

## Requirements

- Python 3.7+
- Streamlit
- OpenAI API key
- YouTube Transcript API
- deep-translator
- langdetect
- requests

Full requirements are listed in `requirements.txt`

## Project Structure

```
video-summarizer/
│
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (create this)
├── images/
│   ├── logo.svg         # Application logo
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for their powerful GPT-3.5 model
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction
- [Streamlit](https://streamlit.io/) for the wonderful web framework

## Support

If you find this project helpful, please give it a ⭐️!

For support, please open an issue in the GitHub repository.
