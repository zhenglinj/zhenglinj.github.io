#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <tuple>

#include <stdio.h>
#include <string.h>

// See http://www-igm.univ-mlv.fr/~lecroq/seqcomp/node4.html.
class LCS
{
	class LCSTable
	{
		size_t   m_;
		size_t   n_;
		size_t*  data_;
	public:
		LCSTable(size_t m, size_t n)
			: m_(m)
			, n_(n)
		{
			data_ = new size_t[(m_ + 1) * (n_ + 1)];
		}
		~LCSTable()
		{
			delete[] data_;
		}

		void setAt(size_t i, size_t j, size_t value)
		{
			data_[i + j * (m_ + 1)] = value;
		}

		size_t getAt(size_t i, size_t j) const
		{
			return data_[i + j * (m_ + 1)];
		}

		template<typename T> void
			build(const T* X, const T* Y)
		{
			for (size_t i = 0; i <= m_; ++i)
				setAt(i, 0, 0);

			for (size_t j = 0; j <= n_; ++j)
				setAt(0, j, 0);

			for (size_t i = 0; i < m_; ++i)
			{
				for (size_t j = 0; j < n_; ++j)
				{
					if (X[i] == Y[j])
						setAt(i + 1, j + 1, getAt(i, j) + 1);
					else
						setAt(i + 1, j + 1, std::max(getAt(i + 1, j), getAt(i, j + 1)));
				}
			}
		}
	};

	template<typename T> static void
		backtrackOne(const LCSTable& table,
		const T* X, const T* Y, size_t i, size_t j,
		std::vector<T>& result)
	{
		result.clear();
		if (i == 0 || j == 0)
			return;
		if (X[i - 1] == Y[j - 1])
		{
			backtrackOne(table, X, Y, i - 1, j - 1, result);
			result.push_back(X[i - 1]);
			return;
		}
		if (table.getAt(i, j - 1) > table.getAt(i - 1, j))
			backtrackOne(table, X, Y, i, j - 1, result);
		else
			backtrackOne(table, X, Y, i - 1, j, result);
	}

	template<typename T> static void
		backtrackAll(const LCSTable& table,
		const T* X, const T* Y, size_t i, size_t j,
		std::vector<std::tuple<char, T>>& all_result)
	{
		all_result.clear();
		if (i == 0 && j == 0)
			return;
		if (i > 0 && j > 0 && X[i - 1] == Y[j - 1])
		{
			backtrackAll(table, X, Y, i - 1, j - 1, all_result);
			all_result.push_back(std::make_tuple(' ', X[i - 1]));
		}
		else if (i == 0 || table.getAt(i, j - 1) >= table.getAt(i - 1, j))
		{
			backtrackAll(table, X, Y, i, j - 1, all_result);
			all_result.push_back(std::make_tuple('+', Y[j - 1]));
		}
		else if (j == 0 || table.getAt(i, j - 1) < table.getAt(i - 1, j))
		{
			backtrackAll(table, X, Y, i - 1, j, all_result);
			all_result.push_back(std::make_tuple('-', X[i - 1]));
		}
	}

public:
	template<typename T> static void
		findOne(T* X, size_t m, T* Y, size_t n,
		std::vector<T>& result)
	{
		LCSTable table(m, n);
		table.build(X, Y);
		backtrackOne(table, X, Y, m, n, result);
	}

	template<typename T> static void
		findAll(T* X, size_t m, T* Y, size_t n,
		std::vector<std::tuple<char, T>>& all_result)
	{
		LCSTable table(m, n);
		table.build(X, Y);
		backtrackAll(table, X, Y, m, n, all_result);
	}
};

int main()
{
	//char X[] = "XMJYAUZ";
	//char Y[] = "MZJAWXU";
	//std::vector<char> result;
	//LCS::findOne(X, strlen(X), Y, strlen(Y), result);
	//std::string resultString(&result.front(), result.size());
	//std::cout << resultString << std::endl;

	std::string strs1[] = {
		"This part of the document has stayed",
		"the same from version to version.",
		"",
		"This paragraph contains text that is",
		"outdated - it will be deprecated '''and'''",
		"deleted '''in''' the near future.",
		"",
		"It is important to spell check this",
		"dokument. On the other hand, a misspelled",
		"word isn't the end of the world.",
	};
	std::string strs2[] = {
		"This is an important notice! It should",
		"therefore be located at the beginning of",
		"this document!",
		"",
		"This part of the document has stayed",
		"the same from version to version.",
		"",
		"It is important to spell check this",
		"document. On the other hand, a misspelled",
		"word isn't the end of the world. This",
		"paragraph contains important new",
		"additions to this document.",
	};
	std::vector<std::string> result;
	std::vector<std::tuple<char, std::string>> result_all;
	LCS::findAll<std::string>(strs1, sizeof(strs1) / sizeof(std::string),
		strs2, sizeof(strs2) / sizeof(std::string),
		result_all);
	for (std::tuple<char, std::string>& s : result_all)
	{
		std::cout << std::get<0>(s)
			<< " "
			<< std::get<1>(s)
			<< std::endl;
	}

	return 0;
}
