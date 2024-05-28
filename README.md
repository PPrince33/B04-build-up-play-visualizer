# Bayer Leverkusen Build-Up Play Visualizer

This project visualizes the build-up play leading to goals for Bayer Leverkusen, using match data to create interactive visualizations in Streamlit. It utilizes `mplsoccer` for pitch plotting and `matplotlib` for drawing the actions on the pitch.

## Installation

To get started, you need to install the required Python packages. The script includes an installation function that ensures all necessary packages are installed:

1. Clone the Repository:

   ```sh
   git clone https://github.com/yourusername/bayer-leverkusen-build-up-play-visualizer.git
   cd bayer-leverkusen-build-up-play-visualizer
   ```

2. Install the Required Packages:

   You can run the provided installation script or install the packages manually using pip:

   ```sh
   pip install streamlit pandas mplsoccer numpy matplotlib termcolor colored
   ```

## How to Run

1. Run the Streamlit App:

   ```sh
   streamlit run app.py
   ```

   Ensure the CSV files (`B04.csv` and `B04_vs.csv`) are placed correctly in the specified paths.

## File Structure

- `app.py`: Main application script that runs the Streamlit app.
- `B04.csv`: Match data for Bayer Leverkusen.
- `B04_vs.csv`: Data of opponents and match identifiers.

## Usage

When you run the Streamlit app, you will see the following interactive options:

1. **Select the Opponent Team**: Choose the opponent team from a dropdown list.
2. **Select the Match**: Once an opponent team is selected, choose the specific match.
3. **Select the Goal**: Choose the specific goal to visualize the build-up play.

The app will then plot the build-up actions leading to the selected goal on a soccer pitch, with annotations for each action.

## Example

The application provides an interactive visualization of the build-up play leading to goals for Bayer Leverkusen. By selecting the opponent team, match, and specific goal, you can see a detailed plot of actions such as carries, passes, shots, and more.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License.
