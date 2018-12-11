#include <iostream>
#include <sstream>
#include <vector>
#include <thread>

#define MAX_BOARDSIZE 2048
#define NUM           8

using namespace std;

class Queens
{
private:
    vector<int> _chessboard;
    size_t _board_size;
    vector<int> _column_flag, _slash1_flag, _slash2_flag;

    void _print_board() {
        stringstream ss;
        for (auto pos : _chessboard)
            ss << string(2*pos, '_') << "##" << string(2*(_board_size - pos - 1), '_') << "\n";
        ss << "\n";
        cout << ss.str();
    };

    void _place_nrow_queen(int row) {
        for (size_t col = 0; col < _board_size; ++col)
        {
            if (_column_flag[col] == 1
                || _slash1_flag[row + col] == 1
                || _slash2_flag[row - col + _board_size - 1] == 1)
                continue;

            _chessboard[row] = col;
            _column_flag[col] = 1;
            _slash1_flag[row + col] = 1;
            _slash2_flag[row - col + _board_size - 1] = 1;

            if (row > 0)
                _place_nrow_queen(row - 1);
            else
                _print_board();

            _chessboard[row] = -1;
            _column_flag[col] = 0;
            _slash1_flag[row + col] = 0;
            _slash2_flag[row - col + _board_size - 1] = 0;
        }
    };

public:
    Queens(size_t board_size = NUM) {
        if (board_size > MAX_BOARDSIZE)
            _board_size = MAX_BOARDSIZE;
        else
            _board_size = board_size;
        _chessboard.resize(board_size, -1);
        _column_flag.resize(board_size, 0);
        _slash1_flag.resize(2*board_size - 1, 0);
        _slash2_flag.resize(2*board_size - 1, 0);
    };
    virtual ~Queens() {};

    void place_all_queens() {
        _place_nrow_queen(_board_size - 1);
    };

    void place_queens_multithread() {
        ;
    };

    // static void __stdcall process_queens(void* param) {
    //     ;
    // };
};


int main(int argc, char *argv[])
{
    Queens queens_test(8);
    queens_test.place_all_queens();

    return 0;
}
