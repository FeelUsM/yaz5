#include <iostream>
#include <vector>

void Solve(std::istream& in = std::cin, std::ostream& out = std::cout) {
    int n, m;
    in >> n >> m;
    std::vector<std::vector<int>> dp(n, std::vector<int>(m, 0));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            char c;
            in >> c;
            if (c == '.') {
                continue;
            }
            if (i > 0 && j > 0) {
                dp[i][j] = std::min(dp[i - 1][j], std::min(dp[i - 1][j - 1], dp[i][j - 1])) + 1;
            } else {
                dp[i][j] = 1;
            }
        }
    }
    int max_k = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            int k = dp[i][j];
            if (k > max_k &&
                    ((i + 2 * k < n && j - k >= 0 && j + k < m && dp[i + k][j - k] >= k && dp[i + k][j] >= k && dp[i + k][j + k] >= k && dp[i + 2 * k][j] >= k) ||
                    (i - k >= 0 && i + k < n && j + 2 * k < m && dp[i][j + k] >= k && dp[i][j + 2 * k] >= k && dp[i - k][j + k] >= k && dp[i + k][j + k] >= k) ||
                    (i - k >= 0 && i + k < n && j - k >= 0 && j + k < m && dp[i][j - k] >= k && dp[i][j + k] >= k && dp[i - k][j] >= k && dp[i + k][j] >= k) ||
                    (i - k >= 0 && i + k < n && j - 2 * k >= 0 && dp[i][j - 2 * k] >= k && dp[i][j - k] >= k && dp[i - k][j - k] >= k && dp[i + k][j - k] >= k) ||
                    (i - 2 * k >= 0 && j - k >= 0 && j + k < m && dp[i - k][j - k] >= k && dp[i - k][j] >= k && dp[i - k][j + k] >= k && dp[i - 2 * k][j] >= k))) {
                max_k = k;
            }
        }
    }
    out << max_k << '\n';
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(nullptr);
    Solve();
    return 0;
}
