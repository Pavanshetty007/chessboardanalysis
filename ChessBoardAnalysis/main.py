from chessboardanalyzer import ChessboardAnalyzer
from config import PATH
# Usage Example
if __name__ == "__main__":

    # Create an instance of ChessboardAnalyzer
    analyzer = ChessboardAnalyzer(PATH.INPUT_DIR)

    # Run the analysis
    analyzer.run()
