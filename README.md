# GitHub Spider

GitHub Spider is a Python script that interacts with the GitHub API to crawl user profiles, follow users based on follower count, display user repositories, and star repositories that meet popularity criteria.

## Features

- **User Crawling**: Fetches and displays GitHub user profiles.
- **Following Users**: Automatically follows GitHub users with over 300 followers.
- **Repository Handling**: Displays and stars repositories based on popularity.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Ian729/GithubSpider.git
   cd GithubSpider
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your GitHub token as an environment variable:

   ```bash
   export GITHUB_TOKEN=your-github-token
   ```

   Replace `your-github-token` with your actual GitHub personal access token.

2. Modify the script (`github_spider.py`) to customize crawling depth (`DEPTH_LIMIT`) and other parameters as needed.

3. Run the script:

   ```bash
   python github_spider.py
   ```

   The script will start crawling from a predefined GitHub user (`Ian729` by default) and follow users, display repositories, and star popular repositories.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### Notes:

- **GitHub Token**: Ensure your GitHub token (`GITHUB_TOKEN`) is set properly in your environment variables to avoid unauthorized access errors.
- **Customization**: Modify the script (`github_spider.py`) to adjust parameters like `DEPTH_LIMIT`, follower count criteria, and repository popularity thresholds according to your requirements.
- **Dependencies**: Check and update `requirements.txt` as your project evolves and new dependencies are added.

This README.md template provides an overview of your project, installation instructions, usage guidelines, contribution information, and licensing details. Customize it further based on specific details and features of your GitHub Spider project.