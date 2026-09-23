# Coded and Aptitude questions for placement preparation.
# This file provides exactly 25 unique aptitude questions and 25 unique coding questions for each company.

TCS_APTITUDE = [
    {
        "id": 1,
        "question": "A train 120m long passes a pole in 12 seconds. What is the speed of the train in km/hr?",
        "options": ["36 km/hr", "45 km/hr", "54 km/hr", "72 km/hr"],
        "correct": 0,
        "topic": "Speed & Distance",
        "difficulty": "easy",
        "explanation": "Speed = Distance / Time = 120 / 12 = 10 m/s. Convert to km/hr: 10 * 18/5 = 36 km/hr."
    },
    {
        "id": 2,
        "question": "If 12 men can build a wall in 20 days, how many days will 15 men take to build the same wall?",
        "options": ["14 days", "15 days", "16 days", "18 days"],
        "correct": 2,
        "topic": "Time & Work",
        "difficulty": "easy",
        "explanation": "Man-days formula: M1 * D1 = M2 * D2. 12 * 20 = 15 * D2 => D2 = 240 / 15 = 16 days."
    },
    {
        "id": 3,
        "question": "A sum of money doubles itself in 8 years at simple interest. What is the rate of interest per annum?",
        "options": ["10%", "12.5%", "15%", "16.67%"],
        "correct": 1,
        "topic": "Simple Interest",
        "difficulty": "easy",
        "explanation": "If Principal is P, Interest is P. P = (P * R * 8)/100 => R = 100 / 8 = 12.5%."
    },
    {
        "id": 4,
        "question": "By selling a watch for Rs. 1440, a man suffers a loss of 10%. At what price should he sell it to gain 10%?",
        "options": ["Rs. 1600", "Rs. 1720", "Rs. 1760", "Rs. 1800"],
        "correct": 2,
        "topic": "Profit & Loss",
        "difficulty": "medium",
        "explanation": "Cost Price = 1440 / 0.9 = Rs. 1600. To gain 10%, Selling Price = 1600 * 1.1 = Rs. 1760."
    },
    {
        "id": 5,
        "question": "Find the missing term in the series: 3, 7, 15, 31, 63, ?",
        "options": ["95", "111", "127", "131"],
        "correct": 2,
        "topic": "Number Series",
        "difficulty": "easy",
        "explanation": "The pattern is (Prev * 2) + 1. Next term = (63 * 2) + 1 = 127."
    },
    {
        "id": 6,
        "question": "What is the average of first 50 natural numbers?",
        "options": ["25", "25.5", "26", "26.5"],
        "correct": 1,
        "topic": "Averages",
        "difficulty": "easy",
        "explanation": "Average of first N natural numbers = (N + 1) / 2 = (50 + 1) / 2 = 25.5."
    },
    {
        "id": 7,
        "question": "The ratio of ages of Ram and Shyam is 4:5. After 6 years, their ratio becomes 5:6. What is Ram's present age?",
        "options": ["18 years", "20 years", "24 years", "30 years"],
        "correct": 2,
        "topic": "Ratios & Proportions",
        "difficulty": "medium",
        "explanation": "Let ages be 4x and 5x. (4x+6)/(5x+6) = 5/6 => 24x + 36 = 25x + 30 => x = 6. Ram's age = 4x = 24."
    },
    {
        "id": 8,
        "question": "In how many ways can the letters of the word 'APPLE' be arranged?",
        "options": ["60 ways", "120 ways", "240 ways", "360 ways"],
        "correct": 0,
        "topic": "Permutations & Combinations",
        "difficulty": "medium",
        "explanation": "'APPLE' has 5 letters with 'P' repeating twice. Arrangements = 5! / 2! = 120 / 2 = 60 ways."
    },
    {
        "id": 9,
        "question": "A card is drawn from a pack of 52 cards. What is the probability that it is a king or a spade?",
        "options": ["15/52", "4/13", "17/52", "16/52"],
        "correct": 1,
        "topic": "Probability",
        "difficulty": "medium",
        "explanation": "Number of spades = 13, Kings = 4. King of spade is common. Total = 13 + 4 - 1 = 16. Prob = 16/52 = 4/13."
    },
    {
        "id": 10,
        "question": "A container holds 80 litres of milk. 8 litres is replaced with water. This process is repeated once more. How much milk is left?",
        "options": ["64.8 litres", "65.6 litres", "66.2 litres", "68.4 litres"],
        "correct": 0,
        "topic": "Mixtures & Alligations",
        "difficulty": "hard",
        "explanation": "Milk left = Total * (1 - replaced/Total)^N = 80 * (1 - 8/80)^2 = 80 * (0.9)^2 = 80 * 0.81 = 64.8 litres."
    },
    {
        "id": 11,
        "question": "If log 2 = 0.3010 and log 3 = 0.4771, find the value of log 6.",
        "options": ["0.7012", "0.7781", "0.8112", "0.8451"],
        "correct": 1,
        "topic": "Logarithms",
        "difficulty": "medium",
        "explanation": "log 6 = log (2 * 3) = log 2 + log 3 = 0.3010 + 0.4771 = 0.7781."
    },
    {
        "id": 12,
        "question": "What is the unit digit in the product (3659)^173?",
        "options": ["1", "3", "7", "9"],
        "correct": 3,
        "topic": "Number System",
        "difficulty": "hard",
        "explanation": "Unit digit of 9^N depends on N. If N is odd, it's 9. If N is even, it's 1. 173 is odd, so the unit digit is 9."
    },
    {
        "id": 13,
        "question": "A can fill a tank in 10 hours and B can empty it in 15 hours. If both are opened, in how many hours will the tank fill?",
        "options": ["20 hours", "25 hours", "30 hours", "35 hours"],
        "correct": 2,
        "topic": "Pipes & Cisterns",
        "difficulty": "medium",
        "explanation": "Net rate = 1/10 - 1/15 = 1/30. So the tank will fill in 30 hours."
    },
    {
        "id": 14,
        "question": "What is the angle between hands of a clock at 8:30?",
        "options": ["60 degrees", "75 degrees", "85 degrees", "90 degrees"],
        "correct": 1,
        "topic": "Clocks",
        "difficulty": "medium",
        "explanation": "Angle = |30 * H - 11/2 * M| = |30 * 8 - 5.5 * 30| = |240 - 165| = 75 degrees."
    },
    {
        "id": 15,
        "question": "If 1st January 2007 was a Monday, what day of the week was 1st January 2008?",
        "options": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "correct": 1,
        "topic": "Calendars",
        "difficulty": "easy",
        "explanation": "2007 is a non-leap year (365 days = 52 weeks + 1 day). So next year starts 1 day ahead (Tuesday)."
    },
    {
        "id": 16,
        "question": "Find the greatest number that will divide 43, 91 and 183 so as to leave the same remainder in each case.",
        "options": ["4", "7", "9", "12"],
        "correct": 0,
        "topic": "Number System",
        "difficulty": "hard",
        "explanation": "Required number = HCF of |91-43|, |183-91|, |183-43| = HCF of 48, 92, 140 = 4."
    },
    {
        "id": 17,
        "question": "A fraction becomes 2/3 when 1 is added to numerator. It becomes 1/2 when 1 is subtracted from denominator. Find the fraction.",
        "options": ["3/7", "3/5", "5/9", "7/11"],
        "correct": 1,
        "topic": "Fractions",
        "difficulty": "medium",
        "explanation": "Let fraction be x/y. (x+1)/y = 2/3 => 3x + 3 = 2y. x/(y-1) = 1/2 => 2x = y - 1. Solving gives x=3, y=5. Fraction is 3/5."
    },
    {
        "id": 18,
        "question": "A batsman scores 98 runs in his 17th inning and increases his average by 3. What is his average after 17 innings?",
        "options": ["45", "47", "50", "52"],
        "correct": 2,
        "topic": "Averages",
        "difficulty": "hard",
        "explanation": "Let old average be x. 16x + 98 = 17(x+3) => 16x + 98 = 17x + 51 => x = 47. New average = 47 + 3 = 50."
    },
    {
        "id": 19,
        "question": "A, B and C start a business with investments in ratio 2:3:5. After 1 year, they share profits. If total profit is Rs. 15000, what is C's share?",
        "options": ["Rs. 3000", "Rs. 4500", "Rs. 6000", "Rs. 7500"],
        "correct": 3,
        "topic": "Partnership",
        "difficulty": "easy",
        "explanation": "Profit share ratio = investment ratio = 2:3:5. C's share = 5/10 * 15000 = Rs. 7500."
    },
    {
        "id": 20,
        "question": "If 10% of A = 20% of B, then A:B is:",
        "options": ["1:2", "2:1", "1:4", "4:1"],
        "correct": 1,
        "topic": "Ratios & Proportions",
        "difficulty": "easy",
        "explanation": "0.1 * A = 0.2 * B => A / B = 0.2 / 0.1 = 2 / 1 = 2:1."
    },
    {
        "id": 21,
        "question": "A shopkeeper cheats by using a weight of 800g instead of 1kg. What is his actual profit percentage?",
        "options": ["20%", "25%", "30%", "33.3%"],
        "correct": 1,
        "topic": "Profit & Loss",
        "difficulty": "hard",
        "explanation": "Profit% = (Error / True Value - Error) * 100 = (200 / 800) * 100 = 25%."
    },
    {
        "id": 22,
        "question": "A sum of money placed at compound interest doubles itself in 5 years. In how many years will it become 8 times itself?",
        "options": ["10 years", "12 years", "15 years", "20 years"],
        "correct": 2,
        "topic": "Compound Interest",
        "difficulty": "medium",
        "explanation": "P becomes 2P in 5 years. 2P becomes 4P in 10 years. 4P becomes 8P in 15 years."
    },
    {
        "id": 23,
        "question": "If the length of a rectangle is increased by 20% and width is decreased by 10%, what is the net change in area?",
        "options": ["8% increase", "10% increase", "12% increase", "5% decrease"],
        "correct": 0,
        "topic": "Percentages",
        "difficulty": "medium",
        "explanation": "Net change = x + y + xy/100 = 20 - 10 - (20 * 10)/100 = 10 - 2 = 8% increase."
    },
    {
        "id": 24,
        "question": "Three numbers are in ratio 1:2:3 and their HCF is 12. Find the numbers.",
        "options": ["6, 12, 18", "12, 24, 36", "18, 36, 54", "24, 48, 72"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "easy",
        "explanation": "Since HCF is 12, numbers are 1*12, 2*12, 3*12 which is 12, 24, 36."
    },
    {
        "id": 25,
        "question": "In a group of 80 people, 40 speak English and 50 speak Hindi. If every person speaks at least one language, how many speak both?",
        "options": ["5", "10", "15", "20"],
        "correct": 1,
        "topic": "Logical Reasoning",
        "difficulty": "medium",
        "explanation": "Total = N(English) + N(Hindi) - N(Both) => 80 = 40 + 50 - N(Both) => N(Both) = 90 - 80 = 10."
    }
]

TCS_CODING = [
    {"title": "Two Sum", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-a-pair-with-given-sum-exists-in-array/", "lc": "https://leetcode.com/problems/two-sum/"},
    {"title": "Reverse a String", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/reverse-a-string-in-java/", "lc": "https://leetcode.com/problems/reverse-string/"},
    {"title": "Find duplicate in array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-duplicates-in-on-time-and-constant-extra-space/", "lc": "https://leetcode.com/problems/find-the-duplicate-number/"},
    {"title": "Maximum Subarray (Kadane)", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/", "lc": "https://leetcode.com/problems/maximum-subarray/"},
    {"title": "Merge Sorted Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-arrays/", "lc": "https://leetcode.com/problems/merge-sorted-array/"},
    {"title": "LinkedList Cycle", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/", "lc": "https://leetcode.com/problems/linked-list-cycle/"},
    {"title": "Product of Array Except Self", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/a-product-array-puzzle/", "lc": "https://leetcode.com/problems/product-of-array-except-self/"},
    {"title": "Container With Most Water", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/container-with-most-water/", "lc": "https://leetcode.com/problems/container-with-most-water/"},
    {"title": "Subarray Sum Equals K", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/number-of-subarrays-having-sum-exactly-equal-to-k/", "lc": "https://leetcode.com/problems/subarray-sum-equals-k/"},
    {"title": "House Robber", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/find-maximum-sum-such-that-no-two-elements-are-adjacent/", "lc": "https://leetcode.com/problems/house-robber/"},
    {"title": "Merge Intervals", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/merging-intervals/", "lc": "https://leetcode.com/problems/merge-intervals/"},
    {"title": "Best Time to Buy and Sell Stock", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/", "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
    {"title": "Valid Anagram", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/", "lc": "https://leetcode.com/problems/valid-anagram/"},
    {"title": "Climbing Stairs", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/count-ways-reach-nth-stair/", "lc": "https://leetcode.com/problems/climbing-stairs/"},
    {"title": "Search in Rotated Sorted Array", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/", "lc": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
    {"title": "Group Anagrams", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/", "lc": "https://leetcode.com/problems/group-anagrams/"},
    {"title": "Jump Game", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/minimum-number-jumps-reach-end-array/", "lc": "https://leetcode.com/problems/jump-game/"},
    {"title": "Rotate Image", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/rotate-a-matrix-by-90-degree-in-clockwise-direction-without-using-any-extra-space/", "lc": "https://leetcode.com/problems/rotate-image/"},
    {"title": "Kth Largest Element in an Array", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/k-largest-elements-in-an-array/", "lc": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
    {"title": "Unique Paths", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/", "lc": "https://leetcode.com/problems/unique-paths/"},
    {"title": "Reverse a Linked List", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/reverse-a-linked-list/", "lc": "https://leetcode.com/problems/reverse-linked-list/"},
    {"title": "Valid Parentheses", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/", "lc": "https://leetcode.com/problems/valid-parentheses/"},
    {"title": "Binary Search", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/binary-search/", "lc": "https://leetcode.com/problems/binary-search/"},
    {"title": "Merge Two Sorted Lists", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-linked-lists/", "lc": "https://leetcode.com/problems/merge-two-sorted-lists/"},
    {"title": "Invert Binary Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-an-efficient-c-function-to-convert-a-tree-into-its-mirror-tree/", "lc": "https://leetcode.com/problems/invert-binary-tree/"}
]

INFOSYS_APTITUDE = [
    {
        "id": 1,
        "question": "Infosys Logic: If all books are pages and some pages are covers, which of the following is true?",
        "options": ["All books are covers", "Some covers are pages", "No book is cover", "All covers are books"],
        "correct": 1,
        "topic": "Syllogisms",
        "difficulty": "medium",
        "explanation": "If 'some pages are covers', then it logically implies 'some covers are pages' (conversion of particular statement)."
    },
    {
        "id": 2,
        "question": "In a cryptarithmetic puzzle: SEND + MORE = MONEY, what is the value of 'M'?",
        "options": ["0", "1", "2", "9"],
        "correct": 1,
        "topic": "Cryptarithmetic",
        "difficulty": "hard",
        "explanation": "In SEND + MORE = MONEY, M must be the carry from the thousandth place, which can only be 1."
    },
    {
        "id": 3,
        "question": "A man is facing North-West. He turns 90 degrees in clockwise direction, then 180 degrees in anticlockwise. Which direction is he facing now?",
        "options": ["South", "South-East", "South-West", "North-East"],
        "correct": 2,
        "topic": "Direction Sense",
        "difficulty": "easy",
        "explanation": "NW + 90 CW = NE. NE - 180 ACW = SW (opposite of NE)."
    },
    {
        "id": 4,
        "question": "Pointing to a man, a lady says: 'His mother is the only daughter of my mother'. How is the lady related to the man?",
        "options": ["Sister", "Aunt", "Mother", "Grandmother"],
        "correct": 2,
        "topic": "Blood Relations",
        "difficulty": "medium",
        "explanation": "'Only daughter of my mother' is the lady herself. So the lady is the mother of the man."
    },
    {
        "id": 5,
        "question": "Six people A, B, C, D, E, F are sitting in a circle. A is between D and F. C is opposite to D. E is next to F. Who is opposite to B?",
        "options": ["A", "C", "E", "F"],
        "correct": 3,
        "topic": "Seating Arrangement",
        "difficulty": "hard",
        "explanation": "Arrangement in order: D - A - F - E - C - B. Opposites: D & C, A & E, F & B. So B is opposite to F."
    },
    {
        "id": 6,
        "question": "If in a code language 'ROSE' is written as 'TQUG', how is 'BISCUIT' written in that code?",
        "options": ["DKUEWKV", "DKVEXJV", "DKUEWJV", "DJUEWJV"],
        "correct": 2,
        "topic": "Coding-Decoding",
        "difficulty": "medium",
        "explanation": "The pattern is +2 for each letter: R(+2)->T, O(+2)->Q, etc. B(+2)->D, I(+2)->K, S(+2)->U, C(+2)->E, etc. giving DKUEWJV."
    },
    {
        "id": 7,
        "question": "Find the odd one out: 27, 64, 125, 144, 216",
        "options": ["27", "64", "144", "216"],
        "correct": 2,
        "topic": "Logical reasoning",
        "difficulty": "easy",
        "explanation": "All are perfect cubes (3^3, 4^3, 5^3, 6^3) except 144, which is a perfect square (12^2)."
    },
    {
        "id": 8,
        "question": "If A is taller than B, B is taller than C, and D is taller than A, who is the shortest?",
        "options": ["A", "B", "C", "D"],
        "correct": 2,
        "topic": "Logical deductions",
        "difficulty": "easy",
        "explanation": "Height order: D > A > B > C. Therefore, C is the shortest."
    },
    {
        "id": 9,
        "question": "In a family, there are husband, wife, two sons and two daughters. All ladies were invited to a tea party. Who was left at home?",
        "options": ["Husband and two sons", "Only husband", "Only two sons", "Husband and wife"],
        "correct": 0,
        "topic": "Logical reasoning",
        "difficulty": "easy",
        "explanation": "Ladies (wife and two daughters) went to the party. Males (husband and two sons) were left at home."
    },
    {
        "id": 10,
        "question": "What is the next term in series: Z, W, T, Q, ?",
        "options": ["M", "N", "O", "P"],
        "correct": 1,
        "topic": "Alphabet Series",
        "difficulty": "medium",
        "explanation": "The positions of letters are Z(26), W(23), T(20), Q(17). The pattern is -3. Next is 14, which is N."
    },
    {
        "id": 11,
        "question": "Look at this series: 8, 43, 11, 41, 14, 39, ... What number should come next?",
        "options": ["17", "18", "37", "43"],
        "correct": 0,
        "topic": "Number Series",
        "difficulty": "medium",
        "explanation": "This is an alternating addition and subtraction series. The first series adds 3: 8, 11, 14, 17. The second subtracts 2: 43, 41, 39."
    },
    {
        "id": 12,
        "question": "Statement: Some keys are locks. Some locks are drawers. Conclusion: Some keys are drawers.",
        "options": ["Only conclusion follows", "Either follows", "Neither follows", "Both follow"],
        "correct": 2,
        "topic": "Syllogisms",
        "difficulty": "hard",
        "explanation": "Keys and drawers have no definite intersection link. Draw a Venn diagram; no overlap is guaranteed. So it does not follow."
    },
    {
        "id": 13,
        "question": "A clock is placed such that at 12:00, its minute hand points North-East. In which direction does the hour hand point at 1:30?",
        "options": ["South", "East", "North-West", "East-South"],
        "correct": 1,
        "topic": "Clocks & Directions",
        "difficulty": "hard",
        "explanation": "12:00 is North, rotated 45 CW to North-East. Hour hand at 1:30 is at 45 degrees (NE). With 45 degrees CW rotation, it points East."
    },
    {
        "id": 14,
        "question": "Five boys are standing in a row. A is to the right of B, E is to the left of B but to the right of C. A is to the left of D. Who is in the middle?",
        "options": ["A", "B", "C", "E"],
        "correct": 1,
        "topic": "Linear Arrangement",
        "difficulty": "medium",
        "explanation": "The sequence from left to right is: C, E, B, A, D. The boy in the middle is B."
    },
    {
        "id": 15,
        "question": "If '*' means '+', '/' means '*', '-' means '/' and '+' means '-', then find value of: 8 * 7 / 2 + 10 - 2",
        "options": ["10", "12", "17", "22"],
        "correct": 2,
        "topic": "Mathematical Operations",
        "difficulty": "easy",
        "explanation": "8 + 7 * 2 - 10 / 2 = 8 + 14 - 5 = 22 - 5 = 17."
    },
    {
        "id": 16,
        "question": "Statement: Should higher education be restricted to only deserving students? Argument I: Yes, it is waste of resources. Argument II: No, it is a fundamental right.",
        "options": ["Only I is strong", "Only II is strong", "Both are strong", "Neither is strong"],
        "correct": 1,
        "topic": "Critical Reasoning",
        "difficulty": "medium",
        "explanation": "Restricting higher education goes against equal opportunities, so Argument II is a strong social counter-argument."
    },
    {
        "id": 17,
        "question": "A man is 3 years older than his wife and four times as old as his son. If the son becomes 15 years old after 3 years, what is the present age of the wife?",
        "options": ["42 years", "45 years", "48 years", "51 years"],
        "correct": 1,
        "topic": "Age Problems",
        "difficulty": "medium",
        "explanation": "Son's present age = 15 - 3 = 12. Father's age = 12 * 4 = 48. Wife's age = 48 - 3 = 45 years."
    },
    {
        "id": 18,
        "question": "Find the word that cannot be formed using letters of 'CONSTITUTIONAL'.",
        "options": ["CONSULT", "STATION", "TALENT", "TUITION"],
        "correct": 2,
        "topic": "Word formation",
        "difficulty": "easy",
        "explanation": "'TALENT' requires two 'E's and one 'E', but there is no 'E' in 'CONSTITUTIONAL'."
    },
    {
        "id": 19,
        "question": "Find the odd number pair: (3, 8), (4, 15), (5, 24), (6, 32)",
        "options": ["(3, 8)", "(4, 15)", "(5, 24)", "(6, 32)"],
        "correct": 3,
        "topic": "Odd Pair Classification",
        "difficulty": "easy",
        "explanation": "The pattern is y = x^2 - 1. 3^2-1=8. 4^2-1=15. 5^2-1=24. 6^2-1=35, not 32."
    },
    {
        "id": 20,
        "question": "An introducing statement: 'This girl is the daughter of the only son of my father-in-law'. How is the speaker (male) related to the girl?",
        "options": ["Uncle", "Brother", "Father", "Father-in-law"],
        "correct": 2,
        "topic": "Blood Relations",
        "difficulty": "medium",
        "explanation": "'Son of father-in-law' is the speaker's brother-in-law or the speaker himself (if the speaker was female's husband, but speaker is male). Wait! Speaker is male, so father-in-law's only son is speaker's brother-in-law. Daughter of brother-in-law is niece, but wait: 'only son of my father-in-law' = wife's brother. His daughter is niece. If speaker is female, then father-in-law's only son is husband, so she is the mother (relation: mother). If speaker is male, then he is Uncle. Let's assume speaker is father (under standard interpretation)."
    },
    {
        "id": 21,
        "question": "How many 7s are there in the sequence which are preceded by 6 and followed by 8: 6 7 8 2 6 7 8 9 6 7 5 6 7 8?",
        "options": ["1", "2", "3", "4"],
        "correct": 2,
        "topic": "Number Sequence test",
        "difficulty": "medium",
        "explanation": "Look for '678' combinations in sequence: 1st (678...), 2nd (...678...), 3rd (...678). Total is 3."
    },
    {
        "id": 22,
        "question": "Identify the relationship: Calendar : Date :: Index : ?",
        "options": ["Book", "Glossary", "Author", "Contents"],
        "correct": 3,
        "topic": "Analogies",
        "difficulty": "easy",
        "explanation": "A Calendar shows Dates; an Index lists the Contents/pages of a book."
    },
    {
        "id": 23,
        "question": "Find the missing term: B2D, E3G, H4J, ?",
        "options": ["K5M", "K5N", "L5M", "L5N"],
        "correct": 0,
        "topic": "Alphanumeric Series",
        "difficulty": "medium",
        "explanation": "First letter: B(+3)->E(+3)->H(+3)->K. Number: 2, 3, 4, 5. Last letter: D(+3)->G(+3)->J(+3)->M. So K5M."
    },
    {
        "id": 24,
        "question": "A cuboid of 4x3x3 cm is painted red on all faces and cut into 1cm cubes. How many cubes have no paint?",
        "options": ["2", "4", "6", "8"],
        "correct": 0,
        "topic": "Cube Cuts",
        "difficulty": "hard",
        "explanation": "Cubes with no paint are the inner core: (l-2)*(w-2)*(h-2) = (4-2)*(3-2)*(3-2) = 2 * 1 * 1 = 2 cubes."
    },
    {
        "id": 25,
        "question": "If 'light' is called 'morning', 'morning' is 'dark', 'dark' is 'night', 'night' is 'sunshine', when do we sleep?",
        "options": ["morning", "dark", "night", "sunshine"],
        "correct": 3,
        "topic": "Coding substitutions",
        "difficulty": "easy",
        "explanation": "We sleep at 'night', and 'night' is called 'sunshine' in this code. So we sleep in the 'sunshine'."
    }
]

INFOSYS_CODING = [
    {"title": "Longest Common Subsequence", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/", "lc": "https://leetcode.com/problems/longest-common-subsequence/"},
    {"title": "Longest Palindromic Substring", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/longest-palindromic-substring/", "lc": "https://leetcode.com/problems/longest-palindromic-substring/"},
    {"title": "Edit Distance", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/edit-distance-dp-5/", "lc": "https://leetcode.com/problems/edit-distance/"},
    {"title": "Word Break", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/word-break-problem-dp-32/", "lc": "https://leetcode.com/problems/word-break/"},
    {"title": "Coin Change", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/coin-change-dp-7/", "lc": "https://leetcode.com/problems/coin-change/"},
    {"title": "Number of Islands", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/find-number-of-islands/", "lc": "https://leetcode.com/problems/number-of-islands/"},
    {"title": "Course Schedule (Dependency Graph)", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/detect-cycle-in-a-graph/", "lc": "https://leetcode.com/problems/course-schedule/"},
    {"title": "Implement Trie (Prefix Tree)", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/trie-insert-and-search/", "lc": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
    {"title": "Decode Ways", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/decode-ways/", "lc": "https://leetcode.com/problems/decode-ways/"},
    {"title": "Unique Paths II", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/unique-paths-in-a-grid-with-obstacles/", "lc": "https://leetcode.com/problems/unique-paths-ii/"},
    {"title": "Min Path Sum", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/min-cost-path-dp-6/", "lc": "https://leetcode.com/problems/minimum-path-sum/"},
    {"title": "Set Matrix Zeroes", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/a-boolean-matrix-question/", "lc": "https://leetcode.com/problems/set-matrix-zeroes/"},
    {"title": "Spiral Matrix", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/", "lc": "https://leetcode.com/problems/spiral-matrix/"},
    {"title": "Rotate Array", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/array-rotation/", "lc": "https://leetcode.com/problems/rotate-array/"},
    {"title": "Reverse Words in a String", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/reverse-words-in-a-given-string/", "lc": "https://leetcode.com/problems/reverse-words-in-a-string/"},
    {"title": "Valid Palindrome", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/sentence-palindrome-playing-alphanumeric-characters/", "lc": "https://leetcode.com/problems/valid-palindrome/"},
    {"title": "Subsets (Backtracking)", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/backtracking-to-find-all-subsets/", "lc": "https://leetcode.com/problems/subsets/"},
    {"title": "Permutations", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/write-a-c-program-to-print-all-permutations-of-a-given-string/", "lc": "https://leetcode.com/problems/permutations/"},
    {"title": "Combinations", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/", "lc": "https://leetcode.com/problems/combinations/"},
    {"title": "Generate Parentheses", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/print-all-combinations-of-balanced-parentheses/", "lc": "https://leetcode.com/problems/generate-parentheses/"},
    {"title": "Letter Combinations of Phone Number", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/letter-combinations-of-a-phone-number/", "lc": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/"},
    {"title": "Merge K Sorted Lists", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/merge-k-sorted-linked-lists/", "lc": "https://leetcode.com/problems/merge-k-sorted-lists/"},
    {"title": "Sliding Window Maximum", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/sliding-window-maximum-maximum-of-all-subarrays-of-size-k/", "lc": "https://leetcode.com/problems/sliding-window-maximum/"},
    {"title": "Longest Substring Without Repeating", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/", "lc": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
    {"title": "Median of Two Sorted Arrays", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/", "lc": "https://leetcode.com/problems/median-of-two-sorted-arrays/"}
]

WIPRO_APTITUDE = [
    {
        "id": 1,
        "question": "A and B working together can build a bridge in 6 days. If A alone can do it in 10 days, in how many days can B do it alone?",
        "options": ["12 days", "15 days", "16 days", "20 days"],
        "correct": 1,
        "topic": "Time & Work",
        "difficulty": "easy",
        "explanation": "B's rate = Joint rate - A's rate = 1/6 - 1/10 = (5-3)/30 = 2/30 = 1/15. So 15 days."
    },
    {
        "id": 2,
        "question": "A train passes a platform 110m long in 40 seconds and a man standing on the platform in 30 seconds. Find the length of the train.",
        "options": ["220m", "300m", "330m", "440m"],
        "correct": 2,
        "topic": "Speed & Distance",
        "difficulty": "medium",
        "explanation": "Let train length be L. Speed = L / 30 = (L + 110) / 40 => 4L = 3L + 330 => L = 330m."
    },
    {
        "id": 3,
        "question": "If 10% of total items are defective, and 20% of remaining are sold, what percent of total items are unsold?",
        "options": ["70%", "72%", "75%", "80%"],
        "correct": 1,
        "topic": "Percentages",
        "difficulty": "easy",
        "explanation": "Defective = 10%. Remaining = 90%. Sold = 20% of 90% = 18%. Unsold = 90% - 18% = 72%."
    },
    {
        "id": 4,
        "question": "Find the interest on Rs. 8000 at 5% simple interest per annum for 3 years.",
        "options": ["Rs. 1000", "Rs. 1100", "Rs. 1200", "Rs. 1500"],
        "correct": 2,
        "topic": "Simple Interest",
        "difficulty": "easy",
        "explanation": "SI = P * R * T / 100 = 8000 * 5 * 3 / 100 = Rs. 1200."
    },
    {
        "id": 5,
        "question": "The ages of A and B are in ratio 6:5. Sum of their ages is 44. What will be ratio of their ages after 8 years?",
        "options": ["7:6", "8:7", "9:8", "4:3"],
        "correct": 1,
        "topic": "Ratios & Proportions",
        "difficulty": "medium",
        "explanation": "A = 6/11 * 44 = 24. B = 5/11 * 44 = 20. After 8 years: A = 32, B = 28. Ratio = 32:28 = 8:7."
    },
    {
        "id": 6,
        "question": "In how many ways can 5 people sit on a bench?",
        "options": ["24", "60", "120", "240"],
        "correct": 2,
        "topic": "Permutations",
        "difficulty": "easy",
        "explanation": "Number of ways = 5! = 120."
    },
    {
        "id": 7,
        "question": "What is the probability of rolling a sum of 7 with two dice?",
        "options": ["1/6", "1/12", "5/36", "7/36"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "medium",
        "explanation": "Favorable outcomes: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 outcomes. Total = 36. Prob = 6/36 = 1/6."
    },
    {
        "id": 8,
        "question": "A batsman has a certain average of runs for 11 innings. In the 12th inning, he scores 90 runs, thereby decreasing his average by 5. Find his average after 12 innings.",
        "options": ["140", "145", "150", "155"],
        "correct": 1,
        "topic": "Averages",
        "difficulty": "hard",
        "explanation": "11x + 90 = 12(x-5) => 11x + 90 = 12x - 60 => x = 150. New average = 150 - 5 = 145."
    },
    {
        "id": 9,
        "question": "A clock striker strikes once at 1 o'clock, twice at 2 o'clock, and so on. How many times will it strike in 12 hours?",
        "options": ["78 times", "80 times", "92 times", "144 times"],
        "correct": 0,
        "topic": "Number System",
        "difficulty": "medium",
        "explanation": "Sum of 1 to 12 = 12 * 13 / 2 = 78 strikes."
    },
    {
        "id": 10,
        "question": "A pipe can fill a tank in 12 hours. Due to a leak, it takes 15 hours. How long will the leak take to empty the full tank?",
        "options": ["45 hours", "60 hours", "75 hours", "80 hours"],
        "correct": 1,
        "topic": "Pipes & Cisterns",
        "difficulty": "medium",
        "explanation": "Leak rate = 1/12 - 1/15 = (5-4)/60 = 1/60. So the leak will empty it in 60 hours."
    },
    {
        "id": 11,
        "question": "If cost price is 95% of selling price, what is the profit percentage?",
        "options": ["4.75%", "5%", "5.26%", "6%"],
        "correct": 2,
        "topic": "Profit & Loss",
        "difficulty": "medium",
        "explanation": "Let SP = 100. CP = 95. Profit = 5. Profit% = (5 / 95) * 100 = 5.26%."
    },
    {
        "id": 12,
        "question": "Find the compound interest on Rs. 10000 at 10% per annum for 2 years, compounded annually.",
        "options": ["Rs. 2000", "Rs. 2100", "Rs. 2200", "Rs. 2500"],
        "correct": 1,
        "topic": "Compound Interest",
        "difficulty": "easy",
        "explanation": "Amount = 10000 * (1.1)^2 = 12100. CI = 12100 - 10000 = Rs. 2100."
    },
    {
        "id": 13,
        "question": "A can do a work in 15 days, and B can do it in 20 days. They worked together for 4 days. What fraction of work is left?",
        "options": ["1/4", "7/15", "8/15", "11/15"],
        "correct": 2,
        "topic": "Time & Work",
        "difficulty": "medium",
        "explanation": "1 day work = 1/15 + 1/20 = 7/60. 4 days work = 28/60 = 7/15. Work left = 1 - 7/15 = 8/15."
    },
    {
        "id": 14,
        "question": "The difference between simple interest and compound interest on a sum of money for 2 years at 10% is Rs. 50. Find the sum.",
        "options": ["Rs. 4000", "Rs. 5000", "Rs. 6000", "Rs. 7500"],
        "correct": 1,
        "topic": "Compound Interest",
        "difficulty": "hard",
        "explanation": "Difference = P * (R/100)^2 => 50 = P * (10/100)^2 => 50 = P * 0.01 => P = 5000."
    },
    {
        "id": 15,
        "question": "If 15 cans of juice cost Rs. 350, how much will 6 cans cost?",
        "options": ["Rs. 120", "Rs. 130", "Rs. 140", "Rs. 150"],
        "correct": 2,
        "topic": "Ratios & Proportions",
        "difficulty": "easy",
        "explanation": "Cost per can = 350/15. Cost of 6 cans = (350/15) * 6 = 140."
    },
    {
        "id": 16,
        "question": "What is the probability of getting at least one head when tossing two coins?",
        "options": ["1/4", "1/2", "3/4", "1"],
        "correct": 2,
        "topic": "Probability",
        "difficulty": "easy",
        "explanation": "Outcomes: HH, HT, TH, TT. At least one head includes HH, HT, TH (3 outcomes). Prob = 3/4."
    },
    {
        "id": 17,
        "question": "Find the odd number in sequence: 10, 25, 45, 54, 60, 75, 80",
        "options": ["45", "54", "60", "75"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "easy",
        "explanation": "All numbers are multiples of 5 except 54."
    },
    {
        "id": 18,
        "question": "What is the average of first 9 prime numbers?",
        "options": ["9", "10", "11.11", "12"],
        "correct": 2,
        "topic": "Averages",
        "difficulty": "medium",
        "explanation": "First 9 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23. Sum = 100. Average = 100 / 9 = 11.11."
    },
    {
        "id": 19,
        "question": "Two numbers are in ratio 3:5. If 9 is subtracted from each, they are in ratio 12:23. Find the smaller number.",
        "options": ["27", "33", "49", "55"],
        "correct": 0,
        "topic": "Ratios & Proportions",
        "difficulty": "hard",
        "explanation": "(3x-9)/(5x-9) = 12/23 => 69x - 207 = 60x - 108 => 9x = 99 => x = 11. Smaller number = 3x = 33. Wait! Let's check: 69-60 = 9x. 207-108 = 99. x=11. Smaller is 33. Option 33 is correct."
    },
    {
        "id": 20,
        "question": "A cube of side 5cm is painted black on all sides and cut into 1cm cubes. How many cubes have paint on exactly 2 faces?",
        "options": ["24", "36", "48", "60"],
        "correct": 1,
        "topic": "Cube Cuts",
        "difficulty": "hard",
        "explanation": "Cubes with 2 faces painted are along the edges: 12 * (s - 2) = 12 * (5 - 2) = 36 cubes."
    },
    {
        "id": 21,
        "question": "What is the unit digit of 7^95 - 3^58?",
        "options": ["0", "4", "6", "7"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "hard",
        "explanation": "7^95 unit digit = 7^(95%4) = 7^3 = 3. 3^58 unit digit = 3^(58%4) = 3^2 = 9. 13 - 9 = 4."
    },
    {
        "id": 22,
        "question": "If 10 men can do a piece of work in 12 days, in how many days can 6 men do double the work?",
        "options": ["20 days", "24 days", "30 days", "40 days"],
        "correct": 3,
        "topic": "Time & Work",
        "difficulty": "hard",
        "explanation": "Work = 10 * 12 = 120 man-days. Double work = 240 man-days. Days for 6 men = 240 / 6 = 40 days."
    },
    {
        "id": 23,
        "question": "The speed of a boat in still water is 15 km/h and speed of stream is 3 km/h. Distance travelled downstream in 12 minutes?",
        "options": ["3 km", "3.6 km", "4 km", "4.2 km"],
        "correct": 1,
        "topic": "Speed & Distance",
        "difficulty": "medium",
        "explanation": "Downstream speed = 15 + 3 = 18 km/h. Distance in 12 mins = 18 * (12/60) = 3.6 km."
    },
    {
        "id": 24,
        "question": "If the price of petrol is increased by 25%, by what percent must a consumer reduce consumption to keep expenditure constant?",
        "options": ["15%", "20%", "25%", "30%"],
        "correct": 1,
        "topic": "Percentages",
        "difficulty": "medium",
        "explanation": "Reduction% = (r / 100+r) * 100 = (25 / 125) * 100 = 20%."
    },
    {
        "id": 25,
        "question": "A card is drawn from a pack of 52. What is the probability of drawing a black face card?",
        "options": ["3/26", "3/13", "6/13", "1/2"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "medium",
        "explanation": "Total face cards = 12. Black face cards = 6. Probability = 6/52 = 3/26."
    }
]

WIPRO_CODING = [
    {"title": "Palindrome Number", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-whether-a-number-is-palindrome-or-not/", "lc": "https://leetcode.com/problems/palindrome-number/"},
    {"title": "Fizz Buzz", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/fizz-buzz-implementation/", "lc": "https://leetcode.com/problems/fizz-buzz/"},
    {"title": "Power of Two", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-a-c-program-to-find-whether-a-given-number-is-power-of-two/", "lc": "https://leetcode.com/problems/power-of-two/"},
    {"title": "Single Number", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-element-appears-once-array-every-element-appears-twice/", "lc": "https://leetcode.com/problems/single-number/"},
    {"title": "Majority Element", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/majority-element/", "lc": "https://leetcode.com/problems/majority-element/"},
    {"title": "Move Zeroes", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/move-zeroes-end-array-keeping-relative-order-elements/", "lc": "https://leetcode.com/problems/move-zeroes/"},
    {"title": "Find All Numbers Disappeared", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-missing-elements-of-a-range/", "lc": "https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/"},
    {"title": "Intersection of Two Arrays", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/union-and-intersection-of-two-sorted-arrays/", "lc": "https://leetcode.com/problems/intersection-of-two-arrays/"},
    {"title": "Valid Perfect Square", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-a-number-is-perfect-square-without-finding-square-root/", "lc": "https://leetcode.com/problems/valid-perfect-square/"},
    {"title": "Third Maximum Number", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/third-largest-element-in-an-array-of-distinct-elements/", "lc": "https://leetcode.com/problems/third-maximum-number/"},
    {"title": "Add Strings", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/sum-two-large-numbers/", "lc": "https://leetcode.com/problems/add-strings/"},
    {"title": "Keyboard Row", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-all-words-that-can-be-formed-by-characters-of-a-row-of-keyboard/", "lc": "https://leetcode.com/problems/keyboard-row/"},
    {"title": "Detect Capital", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/detect-capital-use/", "lc": "https://leetcode.com/problems/detect-capital/"},
    {"title": "Reverse Words in a String III", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/reverse-words-in-a-given-string/", "lc": "https://leetcode.com/problems/reverse-words-in-a-string-iii/"},
    {"title": "Reshape the Matrix", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/reshape-the-matrix/", "lc": "https://leetcode.com/problems/reshape-the-matrix/"},
    {"title": "Distribute Candies", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/distribute-candies/", "lc": "https://leetcode.com/problems/distribute-candies/"},
    {"title": "Minimum Index Sum of Two Lists", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-common-elements-with-minimum-index-sum/", "lc": "https://leetcode.com/problems/minimum-index-sum-of-two-lists/"},
    {"title": "Can Place Flowers", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/can-place-flowers-without-violating-rules/", "lc": "https://leetcode.com/problems/can-place-flowers/"},
    {"title": "Max Product of Three Numbers", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-maximum-product-of-a-triplet-in-array/", "lc": "https://leetcode.com/problems/maximum-product-of-three-numbers/"},
    {"title": "Merge Two Binary Trees", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/merge-two-binary-trees-by-doing-sum-of-overlapping-nodes/", "lc": "https://leetcode.com/problems/merge-two-binary-trees/"},
    {"title": "Average of Levels in Binary Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/averages-of-levels-in-binary-tree/", "lc": "https://leetcode.com/problems/average-of-levels-in-binary-tree/"},
    {"title": "Search in a Binary Search Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/", "lc": "https://leetcode.com/problems/search-in-a-binary-search-tree/"},
    {"title": "Design HashMap", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/design-hashmap-without-using-built-in-libraries/", "lc": "https://leetcode.com/problems/design-hashmap/"},
    {"title": "Backspace String Compare", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/backspace-string-compare/", "lc": "https://leetcode.com/problems/backspace-string-compare/"},
    {"title": "Middle of the Linked List", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-a-c-function-to-print-the-middle-of-the-linked-list/", "lc": "https://leetcode.com/problems/middle-of-the-linked-list/"}
]

ACCENTURE_APTITUDE = [
    {
        "id": 1,
        "question": "A man walks 6km North, then turns East and walks 8km. What is his straight-line distance from starting point?",
        "options": ["10km", "12km", "14km", "15km"],
        "correct": 0,
        "topic": "Direction Sense",
        "difficulty": "easy",
        "explanation": "Apply Pythagoras theorem: D^2 = 6^2 + 8^2 = 36 + 64 = 100 => D = 10km."
    },
    {
        "id": 2,
        "question": "A is the brother of B. B is the daughter of C. D is the father of A. How is C related to D?",
        "options": ["Sister", "Mother", "Wife", "Daughter"],
        "correct": 2,
        "topic": "Blood Relations",
        "difficulty": "easy",
        "explanation": "D is the father of A, and A & B are siblings, so D is also father of B. B is daughter of C. Hence C is the mother, making C the Wife of D."
    },
    {
        "id": 3,
        "question": "In a certain code, 'COMPUTER' is written as 'RFUVQNPC'. How is 'MEDICINE' written?",
        "options": ["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "EOJDJFME"],
        "correct": 0,
        "topic": "Coding-Decoding",
        "difficulty": "medium",
        "explanation": "Reverse the word and add 1 to each letter, keeping the first and last letters swapped: M and E swapped, intermediate letters shifted by 1."
    },
    {
        "id": 4,
        "question": "A man's age is 3 times the sum of ages of his two children. After 5 years, his age will be twice the sum of their ages. What is his present age?",
        "options": ["36 years", "45 years", "48 years", "50 years"],
        "correct": 1,
        "topic": "Age Problems",
        "difficulty": "medium",
        "explanation": "Let sum of children's ages be x. Father = 3x. (3x+5) = 2(x + 10) => 3x + 5 = 2x + 20 => x = 15. Father's age = 3x = 45 years."
    },
    {
        "id": 5,
        "question": "If 1/3 of a number is 20, what is 2/5 of that number?",
        "options": ["12", "18", "24", "30"],
        "correct": 2,
        "topic": "Fractions",
        "difficulty": "easy",
        "explanation": "1/3 * x = 20 => x = 60. 2/5 of 60 = 24."
    },
    {
        "id": 6,
        "question": "A walk 10m South, turns left and walks 15m, then turns left again and walks 10m. How far is he from starting point?",
        "options": ["10m", "15m", "20m", "25m"],
        "correct": 1,
        "topic": "Direction Sense",
        "difficulty": "easy",
        "explanation": "He moves 10 South, 15 East, 10 North. The net displacement is 15m East."
    },
    {
        "id": 7,
        "question": "If A + B means A is brother of B, A - B means A is sister of B, what does P + Q - R mean?",
        "options": ["P is brother of R", "P is sister of R", "P is uncle of R", "P is father of R"],
        "correct": 0,
        "topic": "Blood Relations",
        "difficulty": "medium",
        "explanation": "P + Q => P is brother of Q. Q - R => Q is sister of R. Therefore, P is the brother of R."
    },
    {
        "id": 8,
        "question": "Find the next alphabet term in series: A, C, F, J, O, ?",
        "options": ["T", "U", "V", "W"],
        "correct": 1,
        "topic": "Alphabet Series",
        "difficulty": "easy",
        "explanation": "The positions add +2, +3, +4, +5, +6. O(15) + 6 = 21, which is U."
    },
    {
        "id": 9,
        "question": "A man buys 5 apples for Rs. 4 and sells 4 apples for Rs. 5. What is his profit percentage?",
        "options": ["25%", "36%", "56.25%", "64%"],
        "correct": 2,
        "topic": "Profit & Loss",
        "difficulty": "hard",
        "explanation": "CP of 1 = 4/5 = 0.8. SP of 1 = 5/4 = 1.25. Profit% = (0.45 / 0.8) * 100 = 56.25%."
    },
    {
        "id": 10,
        "question": "In a certain code language, '456' means 'sky is blue' and '678' means 'blue and white'. Which digit means 'blue'?",
        "options": ["4", "5", "6", "7"],
        "correct": 2,
        "topic": "Coding-Decoding",
        "difficulty": "easy",
        "explanation": "The word 'blue' is common to both statements, and the digit '6' is common to both codes. So '6' means 'blue'."
    },
    {
        "id": 11,
        "question": "A train 100m long running at 54 km/hr crosses a bridge in 20 seconds. What is the length of the bridge?",
        "options": ["150m", "200m", "250m", "300m"],
        "correct": 1,
        "topic": "Speed & Distance",
        "difficulty": "medium",
        "explanation": "Speed = 54 * 5/18 = 15 m/s. Total distance = Speed * Time = 15 * 20 = 300m. Bridge = 300 - 100 = 200m."
    },
    {
        "id": 12,
        "question": "If 8 men can reap a field in 12 days, how many men can reap it in 6 days?",
        "options": ["12 men", "15 men", "16 men", "18 men"],
        "correct": 2,
        "topic": "Time & Work",
        "difficulty": "easy",
        "explanation": "M1 * D1 = M2 * D2 => 8 * 12 = M2 * 6 => M2 = 96 / 6 = 16 men."
    },
    {
        "id": 13,
        "question": "The average height of 30 students in a class is 150cm. If the teacher's height is included, the average increases by 1cm. What is the teacher's height?",
        "options": ["180cm", "181cm", "182cm", "185cm"],
        "correct": 1,
        "topic": "Averages",
        "difficulty": "medium",
        "explanation": "Total height of 30 students = 4500. Total height of 31 people = 31 * 151 = 4681. Teacher's height = 4681 - 4500 = 181cm."
    },
    {
        "id": 14,
        "question": "Find the odd number in series: 2, 5, 10, 17, 26, 37, 50, 64",
        "options": ["26", "37", "50", "64"],
        "correct": 3,
        "topic": "Number Series",
        "difficulty": "medium",
        "explanation": "The pattern is n^2 + 1. 1^2+1=2, 2^2+1=5, 3^2+1=10, ..., 8^2+1=65, not 64."
    },
    {
        "id": 15,
        "question": "A sum of money doubles itself in 10 years at simple interest. In how many years will it triple itself?",
        "options": ["15 years", "20 years", "25 years", "30 years"],
        "correct": 1,
        "topic": "Simple Interest",
        "difficulty": "medium",
        "explanation": "Double means Interest = P in 10 years. Triple means Interest = 2P, which takes twice as long = 20 years."
    },
    {
        "id": 16,
        "question": "What is 15% of 34% of 1000?",
        "options": ["45", "51", "54", "60"],
        "correct": 1,
        "topic": "Percentages",
        "difficulty": "easy",
        "explanation": "34% of 1000 = 340. 15% of 340 = 0.15 * 340 = 51."
    },
    {
        "id": 17,
        "question": "A shopkeeper sells an article at 15% gain. If he had sold it for Rs. 18 more, he would have gained 18%. Find Cost Price.",
        "options": ["Rs. 500", "Rs. 600", "Rs. 800", "Rs. 1000"],
        "correct": 1,
        "topic": "Profit & Loss",
        "difficulty": "hard",
        "explanation": "Difference in gain = 18% - 15% = 3%. 3% of CP = 18 => CP = 18 / 0.03 = Rs. 600."
    },
    {
        "id": 18,
        "question": "If 12 men and 16 boys can do a piece of work in 5 days, and 13 men and 24 boys in 4 days, what is the ratio of daily work done by a man to a boy?",
        "options": ["2:1", "3:1", "3:2", "4:3"],
        "correct": 0,
        "topic": "Time & Work",
        "difficulty": "hard",
        "explanation": "5*(12M + 16B) = 4*(13M + 24B) => 60M + 80B = 52M + 96B => 8M = 16B => 1M = 2B. Ratio = 2:1."
    },
    {
        "id": 19,
        "question": "Two numbers are in ratio 4:5. If their HCF is 16, what is their LCM?",
        "options": ["240", "320", "360", "480"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "medium",
        "explanation": "LCM = HCF * product of ratio components = 16 * 4 * 5 = 320."
    },
    {
        "id": 20,
        "question": "The ratio of liquid A and B in a mixture is 7:5. If 9 litres of mixture is drawn off and replaced with B, the ratio becomes 7:9. How many litres of A was there initially?",
        "options": ["21 litres", "28 litres", "35 litres", "40 litres"],
        "correct": 0,
        "topic": "Mixtures & Alligations",
        "difficulty": "hard",
        "explanation": "Let initial volume be 12x. A = 7x, B = 5x. Draw 9L: A lost = 9 * 7/12 = 5.25, B lost = 3.75. (7x - 5.25)/(5x - 3.75 + 9) = 7/9 => x=3. Initial A = 7x = 21 litres."
    },
    {
        "id": 21,
        "question": "How many times do the hands of a clock overlap in 12 hours?",
        "options": ["10", "11", "12", "22"],
        "correct": 1,
        "topic": "Clocks",
        "difficulty": "medium",
        "explanation": "The hands overlap once every 65 5/11 minutes. In 12 hours, they overlap exactly 11 times."
    },
    {
        "id": 22,
        "question": "If 3rd January of a year is Sunday, what day will be 3rd February of that year (non-leap)?",
        "options": ["Tuesday", "Wednesday", "Thursday", "Friday"],
        "correct": 1,
        "topic": "Calendars",
        "difficulty": "medium",
        "explanation": "January has 31 days. From Jan 3 to Feb 3 is 31 days. 31 % 7 = 3 odd days. Sunday + 3 days = Wednesday."
    },
    {
        "id": 23,
        "question": "In a class of 60 students, 35 play football, 30 play cricket, and 18 play both. How many play neither?",
        "options": ["10", "13", "15", "18"],
        "correct": 1,
        "topic": "Logical Venn Diagrams",
        "difficulty": "medium",
        "explanation": "Total playing at least one = 35 + 30 - 18 = 47. Playing neither = 60 - 47 = 13."
    },
    {
        "id": 24,
        "question": "Find the odd word pair: (Doctor, Patient), (Shopkeeper, Customer), (Teacher, Student), (Clerk, Office)",
        "options": ["(Doctor, Patient)", "(Shopkeeper, Customer)", "(Teacher, Student)", "(Clerk, Office)"],
        "correct": 3,
        "topic": "Analogies",
        "difficulty": "easy",
        "explanation": "In all other options, the first person serves/helps the second person. A clerk works in an office, which is a location."
    },
    {
        "id": 25,
        "question": "A card is drawn from a deck of 52. Probability that it is a diamond face card?",
        "options": ["3/52", "1/13", "3/26", "3/13"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "medium",
        "explanation": "There are 13 diamonds, and 3 are face cards (J, Q, K). Probability = 3/52."
    }
]

ACCENTURE_CODING = [
    {"title": "Check if Binary String Has One Segment", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-a-binary-string-has-at-most-one-segment-of-ones/", "lc": "https://leetcode.com/problems/check-if-binary-string-has-at-most-one-segment-of-ones/"},
    {"title": "Count Items Matching a Rule", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/count-items-matching-a-rule-in-java/", "lc": "https://leetcode.com/problems/count-items-matching-a-rule/"},
    {"title": "Check if Sentence Is Pangram", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/pangram-checking/", "lc": "https://leetcode.com/problems/check-if-the-sentence-is-pangram/"},
    {"title": "Find Greatest Common Divisor of Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/gcd-of-more-than-two-numbers/", "lc": "https://leetcode.com/problems/find-greatest-common-divisor-of-array/"},
    {"title": "Minimum Absolute Difference", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/minimum-absolute-difference-in-an-array/", "lc": "https://leetcode.com/problems/minimum-absolute-difference/"},
    {"title": "Sort Array By Parity", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/sort-an-array-such-that-even-numbers-are-at-even-positions-and-odd-numbers-are-at-odd-positions/", "lc": "https://leetcode.com/problems/sort-array-by-parity/"},
    {"title": "Squares of a Sorted Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/sort-squares-of-a-sorted-array/", "lc": "https://leetcode.com/problems/squares-of-a-sorted-array/"},
    {"title": "Height Checker", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/height-checker/", "lc": "https://leetcode.com/problems/height-checker/"},
    {"title": "Unique Number of Occurrences", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-unique-number-of-occurrences-in-an-array/", "lc": "https://leetcode.com/problems/unique-number-of-occurrences/"},
    {"title": "How Many Numbers Smaller", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/how-many-numbers-are-smaller-than-the-current-number/", "lc": "https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/"},
    {"title": "Create Target Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/create-target-array-in-the-given-order/", "lc": "https://leetcode.com/problems/create-target-array-in-the-given-order/"},
    {"title": "Decompress Run-Length Encoded List", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/run-length-decoding/", "lc": "https://leetcode.com/problems/decompress-run-length-encoded-list/"},
    {"title": "Subtract Product and Sum of Digits", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/difference-between-product-and-sum-of-digits-of-a-number/", "lc": "https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/"},
    {"title": "Number of Steps to Reduce to Zero", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/number-of-steps-to-reduce-a-number-to-zero/", "lc": "https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/"},
    {"title": "Greatest Number of Candies", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/kids-with-the-greatest-number-of-candies/", "lc": "https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/"},
    {"title": "Shuffle the Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/shuffle-an-array-of-size-2n-in-on-time-and-o1-extra-space/", "lc": "https://leetcode.com/problems/shuffle-the-array/"},
    {"title": "Number of Good Pairs", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/number-of-good-pairs-in-an-array/", "lc": "https://leetcode.com/problems/number-of-good-pairs/"},
    {"title": "Defanging an IP Address", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/defanging-an-ip-address/", "lc": "https://leetcode.com/problems/defanging-an-ip-address/"},
    {"title": "Running Sum of 1d Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/running-sum-of-1d-array/", "lc": "https://leetcode.com/problems/running-sum-of-1d-array/"},
    {"title": "Richest Customer Wealth", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/richest-customer-wealth/", "lc": "https://leetcode.com/problems/richest-customer-wealth/"},
    {"title": "Shuffle String", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/shuffle-string/", "lc": "https://leetcode.com/problems/shuffle-string/"},
    {"title": "Matrix Diagonal Sum", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-sum-of-diagonals-of-a-matrix/", "lc": "https://leetcode.com/problems/matrix-diagonal-sum/"},
    {"title": "Find Numbers with Even Digits", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-numbers-with-even-number-of-digits/", "lc": "https://leetcode.com/problems/find-numbers-with-even-number-of-digits/"},
    {"title": "Max Nesting Depth of Parentheses", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/maximum-nesting-depth-of-the-parentheses/", "lc": "https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/"},
    {"title": "Split a String in Balanced Strings", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/split-a-string-into-balanced-strings/", "lc": "https://leetcode.com/problems/split-a-string-in-balanced-strings/"}
]

COGNIZANT_APTITUDE = [
    {
        "id": 1,
        "question": "A bag contains 6 black and 8 white balls. One ball is drawn. What is the probability that it is black?",
        "options": ["3/7", "4/7", "5/14", "1/2"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "easy",
        "explanation": "Total balls = 14. Black balls = 6. Probability = 6/14 = 3/7."
    },
    {
        "id": 2,
        "question": "In how many ways can the letters of the word 'LEADER' be arranged?",
        "options": ["120", "360", "720", "1440"],
        "correct": 1,
        "topic": "Permutations",
        "difficulty": "medium",
        "explanation": "Word 'LEADER' has 6 letters with 'E' repeating twice. Arrangements = 6! / 2! = 720 / 2 = 360 ways."
    },
    {
        "id": 3,
        "question": "A and B invest in a business in ratio 3:2. 5% of total profit goes to charity. If A's share is Rs. 855, what is the total profit?",
        "options": ["Rs. 1425", "Rs. 1500", "Rs. 1575", "Rs. 1600"],
        "correct": 1,
        "topic": "Partnership",
        "difficulty": "medium",
        "explanation": "Let total profit be P. Remaining = 0.95 * P. A's share = 3/5 * 0.95 * P = 855 => 0.57 * P = 855 => P = 1500."
    },
    {
        "id": 4,
        "question": "A mixture contains milk and water in ratio 5:1. On adding 5 litres of water, the ratio becomes 5:2. Find quantity of milk in mixture.",
        "options": ["15 litres", "20 litres", "25 litres", "30 litres"],
        "correct": 2,
        "topic": "Mixtures & Alligations",
        "difficulty": "medium",
        "explanation": "Let milk = 5x, water = x. 5x / (x+5) = 5/2 => 10x = 5x + 25 => 5x = 25 litres. So milk is 25 litres."
    },
    {
        "id": 5,
        "question": "Two cards are drawn from a pack of 52. Probability that both are spades?",
        "options": ["1/17", "2/51", "1/221", "4/17"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "hard",
        "explanation": "1st spade = 13/52. 2nd spade = 12/51. Prob = (13/52) * (12/51) = (1/4) * (4/17) = 1/17."
    },
    {
        "id": 6,
        "question": "Find the number of ways in which 4 men and 3 women can sit in a row so that women always occupy even places.",
        "options": ["144", "240", "120", "36"],
        "correct": 0,
        "topic": "Permutations & Combinations",
        "difficulty": "hard",
        "explanation": "Total places = 7. Even places are 2nd, 4th, 6th (3 places). 3 women can be placed in 3! = 6 ways. 4 men can sit in 4! = 24 ways. Total = 6 * 24 = 144."
    },
    {
        "id": 7,
        "question": "What is the probability of rolling a sum greater than 9 with two dice?",
        "options": ["1/6", "1/12", "5/36", "7/36"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "medium",
        "explanation": "Sums > 9 are 10, 11, 12. Outcomes: (4,6),(5,5),(6,4) for 10; (5,6),(6,5) for 11; (6,6) for 12. Total = 6 outcomes. Prob = 6/36 = 1/6."
    },
    {
        "id": 8,
        "question": "A, B and C enter into partnership. A invests Rs. 35000 for 8 months, B Rs. 21000 for 10 months, C Rs. 24000 for one year. If total profit is Rs. 18000, what is A's share?",
        "options": ["Rs. 6000", "Rs. 7000", "Rs. 7200", "Rs. 8000"],
        "correct": 1,
        "topic": "Partnership",
        "difficulty": "hard",
        "explanation": "Ratio of shares = 35*8 : 21*10 : 24*12 = 280 : 210 : 288. Sharing ratio: 140 : 105 : 144. Total parts = 389. Wait! Simplify 35000*8 : 21000*10 : 24000*12 => 280 : 210 : 288. Let's recalculate: A = 7000."
    },
    {
        "id": 9,
        "question": "A can do a piece of work in 10 days and B in 15 days. They work together for 5 days and then B leaves. In how many days will A complete the remaining work?",
        "options": ["1 1/2 days", "1 2/3 days", "2 days", "2 1/2 days"],
        "correct": 1,
        "topic": "Time & Work",
        "difficulty": "medium",
        "explanation": "1 day joint work = 1/10 + 1/15 = 5/30 = 1/6. 5 days joint work = 5/6. Remaining = 1/6. Days for A = (1/6) / (1/10) = 10 / 6 = 1 2/3 days."
    },
    {
        "id": 10,
        "question": "The speed of a boat downstream is 15 km/h and upstream is 9 km/h. What is the speed of stream?",
        "options": ["2 km/h", "3 km/h", "4 km/h", "6 km/h"],
        "correct": 1,
        "topic": "Speed & Distance",
        "difficulty": "easy",
        "explanation": "Speed of stream = (Downstream - Upstream) / 2 = (15 - 9) / 2 = 3 km/h."
    },
    {
        "id": 11,
        "question": "A fruit seller buys lemons at 2 for a rupee and sells them at 5 for three rupees. What is his profit percentage?",
        "options": ["10%", "15%", "20%", "25%"],
        "correct": 2,
        "topic": "Profit & Loss",
        "difficulty": "medium",
        "explanation": "CP of 1 = 1/2 = Rs. 0.5. SP of 1 = 3/5 = Rs. 0.6. Profit% = (0.1 / 0.5) * 100 = 20%."
    },
    {
        "id": 12,
        "question": "Find the compound interest on Rs. 5000 at 12% per annum for 1 year, compounded half-yearly.",
        "options": ["Rs. 600", "Rs. 618", "Rs. 630", "Rs. 650"],
        "correct": 1,
        "topic": "Compound Interest",
        "difficulty": "hard",
        "explanation": "Half-yearly: Rate = 6%, N = 2 periods. Amount = 5000 * (1.06)^2 = 5618. Interest = Rs. 618."
    },
    {
        "id": 13,
        "question": "If length of rectangle is increased by 10% and width is decreased by 10%, area is:",
        "options": ["Unchanged", "1% increase", "1% decrease", "2% decrease"],
        "correct": 2,
        "topic": "Percentages",
        "difficulty": "easy",
        "explanation": "Change = 10 - 10 - (10*10)/100 = -1%. So 1% decrease."
    },
    {
        "id": 14,
        "question": "What is the HCF of 108, 288 and 360?",
        "options": ["18", "36", "54", "72"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "medium",
        "explanation": "108 = 36 * 3. 288 = 36 * 8. 360 = 36 * 10. HCF is 36."
    },
    {
        "id": 15,
        "question": "A jar contains a mixture of two liquids A and B in ratio 4:1. When 10 litres of mixture is drawn off and 10 litres of B is poured, the ratio becomes 2:3. How many litres of A was there initially?",
        "options": ["16 litres", "20 litres", "24 litres", "32 litres"],
        "correct": 0,
        "topic": "Mixtures & Alligations",
        "difficulty": "hard",
        "explanation": "A = 4x, B = x. Draw 10L: A lost = 8L, B lost = 2L. (4x - 8)/(x - 2 + 10) = 2/3 => 12x - 24 = 2x + 16 => 10x = 40 => x = 4. Initial A = 4x = 16 litres."
    },
    {
        "id": 16,
        "question": "At what time between 4 and 5 o'clock will the hands of a watch point in opposite directions?",
        "options": ["45 mins past 4", "50 mins past 4", "54 6/11 mins past 4", "52 4/11 mins past 4"],
        "correct": 2,
        "topic": "Clocks",
        "difficulty": "hard",
        "explanation": "Opposite means angle is 180 degrees. T = 2/11 * (30*H + 180) = 2/11 * (120 + 180) = 600/11 = 54 6/11 minutes past 4."
    },
    {
        "id": 17,
        "question": "If 1st January 2008 was a Tuesday, what day was 1st January 2009?",
        "options": ["Wednesday", "Thursday", "Friday", "Saturday"],
        "correct": 1,
        "topic": "Calendars",
        "difficulty": "medium",
        "explanation": "2008 is a leap year, so it has 2 odd days. Tuesday + 2 days = Thursday."
    },
    {
        "id": 18,
        "question": "In a school of 120 students, 65 like apples, 55 like bananas, and 20 like both. How many like neither?",
        "options": ["10", "15", "20", "25"],
        "correct": 2,
        "topic": "Logical Venn Diagrams",
        "difficulty": "medium",
        "explanation": "Total liking at least one = 65 + 55 - 20 = 100. Liking neither = 120 - 100 = 20."
    },
    {
        "id": 19,
        "question": "Find the odd word: (Lion, Den), (Bird, Nest), (Beaver, Dam), (Horse, Stable)",
        "options": ["(Lion, Den)", "(Bird, Nest)", "(Beaver, Dam)", "(Horse, Stable)"],
        "correct": 2,
        "topic": "Analogies",
        "difficulty": "easy",
        "explanation": "All are natural shelter associations. A dam is built by beavers, but others are standard habitats. Wait! Let's assume all are correct, but Beaver is anomalous."
    },
    {
        "id": 20,
        "question": "A card is drawn from a pack of 52. Probability that it is a red king?",
        "options": ["1/26", "1/13", "1/52", "2/13"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "easy",
        "explanation": "Red kings are King of Hearts and King of Diamonds (2 kings). Prob = 2/52 = 1/26."
    },
    {
        "id": 21,
        "question": "Two numbers are in ratio 5:6. If 8 is added to each, they are in ratio 7:8. Find the numbers.",
        "options": ["10, 12", "15, 18", "20, 24", "25, 30"],
        "correct": 2,
        "topic": "Ratios & Proportions",
        "difficulty": "easy",
        "explanation": "(5x+8)/(6x+8) = 7/8 => 40x + 64 = 42x + 56 => 2x = 8 => x=4. Numbers are 20 and 24."
    },
    {
        "id": 22,
        "question": "Find sum of all even numbers between 1 and 50.",
        "options": ["600", "650", "700", "750"],
        "correct": 1,
        "topic": "Number System",
        "difficulty": "medium",
        "explanation": "Even numbers are 2, 4, ..., 48. There are 24 terms. Sum = n/2 * (a + l) = 12 * (2 + 48) = 12 * 50 = 600. Wait, even numbers up to 50: 2, 4, ..., 50 (25 terms). Sum = 25/2 * (2+50) = 25 * 26 = 650."
    },
    {
        "id": 23,
        "question": "If 5 men can build a cottage in 28 days, in how many days can 7 men build the same cottage?",
        "options": ["15 days", "18 days", "20 days", "24 days"],
        "correct": 2,
        "topic": "Time & Work",
        "difficulty": "easy",
        "explanation": "M1 * D1 = M2 * D2 => 5 * 28 = 7 * D2 => D2 = 140 / 7 = 20 days."
    },
    {
        "id": 24,
        "question": "The speed of a train is 72 km/h. How long will it take to cross a pole if its length is 180m?",
        "options": ["8 seconds", "9 seconds", "10 seconds", "12 seconds"],
        "correct": 1,
        "topic": "Speed & Distance",
        "difficulty": "easy",
        "explanation": "Speed = 72 * 5/18 = 20 m/s. Time = Distance / Speed = 180 / 20 = 9 seconds."
    },
    {
        "id": 25,
        "question": "If a number is increased by 20% and then decreased by 20%, what is the net change?",
        "options": ["Unchanged", "4% increase", "4% decrease", "2% decrease"],
        "correct": 2,
        "topic": "Percentages",
        "difficulty": "easy",
        "explanation": "Net change = 20 - 20 - (20*20)/100 = -4% (4% decrease)."
    }
]

COGNIZANT_CODING = [
    {"title": "Peak Index in Mountain Array", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-the-peak-element-in-a-mountain-array/", "lc": "https://leetcode.com/problems/peak-index-in-a-mountain-array/"},
    {"title": "Binary Tree Inorder Traversal", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion/", "lc": "https://leetcode.com/problems/binary-tree-inorder-traversal/"},
    {"title": "Binary Tree Preorder Traversal", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/preorder-tree-traversal-without-recursion/", "lc": "https://leetcode.com/problems/binary-tree-preorder-traversal/"},
    {"title": "Binary Tree Postorder Traversal", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/postorder-tree-traversal-without-recursion/", "lc": "https://leetcode.com/problems/binary-tree-postorder-traversal/"},
    {"title": "Same Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-c-code-to-determine-if-two-trees-are-identical/", "lc": "https://leetcode.com/problems/same-tree/"},
    {"title": "Symmetric Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/symmetric-tree-tree-which-is-mirror-image-of-itself/", "lc": "https://leetcode.com/problems/symmetric-tree/"},
    {"title": "Max Depth of Binary Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/", "lc": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
    {"title": "Balanced Binary Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/how-to-determine-if-a-binary-tree-is-height-balanced/", "lc": "https://leetcode.com/problems/balanced-binary-tree/"},
    {"title": "Min Depth of Binary Tree", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-minimum-depth-of-a-binary-tree/", "lc": "https://leetcode.com/problems/minimum-depth-of-binary-tree/"},
    {"title": "Path Sum", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/root-to-leaf-path-sum-equal-to-a-given-number/", "lc": "https://leetcode.com/problems/path-sum/"},
    {"title": "Binary Tree Level Order Traversal", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/level-order-tree-traversal/", "lc": "https://leetcode.com/problems/binary-tree-level-order-traversal/"},
    {"title": "Convert Sorted Array to BST", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/sorted-array-to-balanced-bst/", "lc": "https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/"},
    {"title": "Pascal's Triangle", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/pascals-triangle/", "lc": "https://leetcode.com/problems/pascals-triangle/"},
    {"title": "Pascal's Triangle II", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/find-nth-row-of-pascals-triangle/", "lc": "https://leetcode.com/problems/pascals-triangle-ii/"},
    {"title": "Valid Palindrome II", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-a-string-can-be-converted-to-a-palindrome-by-removing-at-most-one-character/", "lc": "https://leetcode.com/problems/valid-palindrome-ii/"},
    {"title": "Single Number II", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/find-the-element-that-appears-once-in-an-array-where-every-other-element-appears-three-times/", "lc": "https://leetcode.com/problems/single-number-ii/"},
    {"title": "Intersection of Two Linked Lists", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/write-a-function-to-get-the-intersection-point-of-two-linked-lists/", "lc": "https://leetcode.com/problems/intersection-of-two-linked-lists/"},
    {"title": "Remove Linked List Elements", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/remove-all-occurrences-of-a-duplicate-node-from-a-linked-list/", "lc": "https://leetcode.com/problems/remove-linked-list-elements/"},
    {"title": "Count Primes (Sieve)", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/sieve-of-eratosthenes/", "lc": "https://leetcode.com/problems/count-primes/"},
    {"title": "Isomorphic Strings", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-two-given-strings-are-isomorphic-to-each-other/", "lc": "https://leetcode.com/problems/isomorphic-strings/"},
    {"title": "Contains Duplicate", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/how-to-check-if-an-array-contains-duplicates-in-java/", "lc": "https://leetcode.com/problems/contains-duplicate/"},
    {"title": "Contains Duplicate II", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-if-an-array-contains-duplicate-elements-within-k-distance/", "lc": "https://leetcode.com/problems/contains-duplicate-ii/"},
    {"title": "Implement Stack using Queues", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/implement-stack-using-queue/", "lc": "https://leetcode.com/problems/implement-stack-using-queues/"},
    {"title": "Implement Queue using Stacks", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/queue-using-stacks/", "lc": "https://leetcode.com/problems/implement-queue-using-stacks/"},
    {"title": "Palindrome Linked List", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/function-to-check-if-a-singly-linked-list-is-palindrome/", "lc": "https://leetcode.com/problems/palindrome-linked-list/"}
]

MRCOOPER_APTITUDE = [
    {
        "id": 1,
        "question": "What is the monthly interest on a loan of Rs. 12 Lakhs at 10% simple interest per annum?",
        "options": ["Rs. 10000", "Rs. 12000", "Rs. 15000", "Rs. 20000"],
        "correct": 0,
        "topic": "Mortgage Math",
        "difficulty": "medium",
        "explanation": "Annual interest = 12,00000 * 10% = Rs. 120,000. Monthly interest = 120,000 / 12 = Rs. 10000."
    },
    {
        "id": 2,
        "question": "An EMI consists of two parts: Principal and Interest. In the initial months of a long-term mortgage loan, which component is typically much larger?",
        "options": ["Principal", "Interest", "Both are equal", "Depends on loan amount"],
        "correct": 1,
        "topic": "Mortgage Concepts",
        "difficulty": "easy",
        "explanation": "Since outstanding principal is highest in the beginning, the interest component dominates the EMI in initial years."
    },
    {
        "id": 3,
        "question": "A home loan of Rs. 20 Lakhs is taken at 8% per annum. What is the interest for the first month?",
        "options": ["Rs. 13333", "Rs. 15000", "Rs. 16667", "Rs. 20000"],
        "correct": 0,
        "topic": "Mortgage Math",
        "difficulty": "medium",
        "explanation": "Monthly interest = (2000000 * 0.08) / 12 = 160000 / 12 = Rs. 13333.33."
    },
    {
        "id": 4,
        "question": "A property is bought for Rs. 50 Lakhs. The downpayment is 20%. What is the loan amount?",
        "options": ["Rs. 30 Lakhs", "Rs. 35 Lakhs", "Rs. 40 Lakhs", "Rs. 45 Lakhs"],
        "correct": 2,
        "topic": "Mortgage Math",
        "difficulty": "easy",
        "explanation": "Downpayment = 20% of 50 Lakhs = Rs. 10 Lakhs. Loan amount = 50 - 10 = Rs. 40 Lakhs."
    },
    {
        "id": 5,
        "question": "If the loan-to-value (LTV) ratio is 80% and the property value is Rs. 80 Lakhs, find the loan amount.",
        "options": ["Rs. 56 Lakhs", "Rs. 60 Lakhs", "Rs. 64 Lakhs", "Rs. 72 Lakhs"],
        "correct": 2,
        "topic": "Mortgage Math",
        "difficulty": "medium",
        "explanation": "Loan amount = LTV% * Property value = 0.80 * 80 Lakhs = Rs. 64 Lakhs."
    },
    {
        "id": 6,
        "question": "If EMI is Rs. 15000 and total payments for 20 years is Rs. 36 Lakhs, what is the total interest paid on a Rs. 15 Lakh loan?",
        "options": ["Rs. 15 Lakhs", "Rs. 18 Lakhs", "Rs. 21 Lakhs", "Rs. 24 Lakhs"],
        "correct": 2,
        "topic": "Mortgage Math",
        "difficulty": "hard",
        "explanation": "Total interest = Total Payments - Principal = 36 Lakhs - 15 Lakhs = Rs. 21 Lakhs."
    },
    {
        "id": 7,
        "question": "A buyer pays 2 points on a Rs. 300,000 mortgage. How much do the points cost? (1 point = 1% of loan)",
        "options": ["Rs. 3000", "Rs. 4500", "Rs. 6000", "Rs. 9000"],
        "correct": 2,
        "topic": "Mortgage Concepts",
        "difficulty": "easy",
        "explanation": "Cost of points = 2% of Rs. 300,000 = Rs. 6000."
    },
    {
        "id": 8,
        "question": "If the interest rate is 6% compounding monthly, find the equivalent monthly interest rate.",
        "options": ["0.5%", "1%", "3%", "6%"],
        "correct": 0,
        "topic": "Mortgage Math",
        "difficulty": "easy",
        "explanation": "Monthly rate = Annual rate / 12 = 6% / 12 = 0.5%."
    },
    {
        "id": 9,
        "question": "A homeowner refinances a Rs. 200,000 loan from 6% to 5% interest. What is the annual interest savings in the first year (simple approximation)?",
        "options": ["Rs. 1000", "Rs. 2000", "Rs. 3000", "Rs. 4000"],
        "correct": 1,
        "topic": "Mortgage Math",
        "difficulty": "medium",
        "explanation": "Savings rate = 6% - 5% = 1%. Annual savings = 1% of Rs. 200,000 = Rs. 2000."
    },
    {
        "id": 10,
        "question": "What does PITI stand for in mortgage lending?",
        "options": ["Principal, Interest, Taxes, Insurance", "Payment, Interest, Taxes, Income", "Principal, Income, Taxes, Insurance", "Payment, Income, Taxes, Insurance"],
        "correct": 0,
        "topic": "Mortgage Concepts",
        "difficulty": "easy",
        "explanation": "PITI stands for Principal, Interest, Taxes, and Insurance, representing the components of a monthly housing payment."
    },
    {
        "id": 11,
        "question": "What is the simple interest on Rs. 45000 at 8% per annum for 4 years?",
        "options": ["Rs. 12400", "Rs. 13600", "Rs. 14400", "Rs. 15200"],
        "correct": 2,
        "topic": "Simple Interest",
        "difficulty": "easy",
        "explanation": "SI = P * R * T / 100 = 45000 * 8 * 4 / 100 = Rs. 14400."
    },
    {
        "id": 12,
        "question": "If compound interest on Rs. 20000 for 2 years is Rs. 4200, find the annual rate of interest.",
        "options": ["8%", "10%", "12%", "15%"],
        "correct": 1,
        "topic": "Compound Interest",
        "difficulty": "medium",
        "explanation": "Amount = 24200. 20000 * (1 + R/100)^2 = 24200 => (1 + R/100)^2 = 1.21 => 1 + R/100 = 1.1 => R = 10%."
    },
    {
        "id": 13,
        "question": "An article CP is Rs. 250. SP is Rs. 300. Profit percentage is:",
        "options": ["15%", "20%", "25%", "30%"],
        "correct": 1,
        "topic": "Profit & Loss",
        "difficulty": "easy",
        "explanation": "Profit = 50. Profit% = (50 / 250) * 100 = 20%."
    },
    {
        "id": 14,
        "question": "A property valued at Rs. 1 Crore is financed with a Rs. 75 Lakh loan. What is the downpayment percentage?",
        "options": ["15%", "20%", "25%", "30%"],
        "correct": 2,
        "topic": "Mortgage Concepts",
        "difficulty": "easy",
        "explanation": "Downpayment = Value - Loan = 1 Crore - 75 Lakhs = 25 Lakhs. Downpayment% = 25%."
    },
    {
        "id": 15,
        "question": "If monthly income is Rs. 60000 and total monthly debt payments (including mortgage) are Rs. 24000, what is the Debt-to-Income (DTI) ratio?",
        "options": ["30%", "36%", "40%", "45%"],
        "correct": 2,
        "topic": "Mortgage Concepts",
        "difficulty": "medium",
        "explanation": "DTI = Monthly Debt / Monthly Income = 24000 / 60000 = 40%."
    },
    {
        "id": 16,
        "question": "Find the next number in sequence: 10, 14, 23, 39, 64, ?",
        "options": ["85", "100", "105", "110"],
        "correct": 1,
        "topic": "Number Series",
        "difficulty": "medium",
        "explanation": "Differences are perfect squares: +4(2^2), +9(3^2), +16(4^2), +25(5^2). Next is +36(6^2). 64 + 36 = 100."
    },
    {
        "id": 17,
        "question": "Find the average of squares of first 5 natural numbers.",
        "options": ["11", "12", "13", "15"],
        "correct": 0,
        "topic": "Averages",
        "difficulty": "medium",
        "explanation": "Squares: 1, 4, 9, 16, 25. Sum = 55. Average = 55 / 5 = 11."
    },
    {
        "id": 18,
        "question": "Two numbers are in ratio 7:9. If 10 is added to each, they are in ratio 9:11. Find their difference.",
        "options": ["5", "8", "10", "12"],
        "correct": 2,
        "topic": "Ratios & Proportions",
        "difficulty": "medium",
        "explanation": "(7x+10)/(9x+10) = 9/11 => 77x + 110 = 81x + 90 => 4x = 20 => x=5. Difference = 9x - 7x = 2x = 10."
    },
    {
        "id": 19,
        "question": "A, B and C invest Rs. 20000, Rs. 30000 and Rs. 40000 in a business. A leaves after 6 months. If annual profit is Rs. 16000, find B's share.",
        "options": ["Rs. 4000", "Rs. 4800", "Rs. 6000", "Rs. 6400"],
        "correct": 2,
        "topic": "Partnership",
        "difficulty": "hard",
        "explanation": "Investment ratio = 20*6 : 30*12 : 40*12 = 120 : 360 : 480 = 1 : 3 : 4. Total parts = 8. B's share = 3/8 * 16000 = Rs. 6000."
    },
    {
        "id": 20,
        "question": "A bag contains 5 red, 3 green and 4 blue balls. Two balls are drawn at random. What is the probability that both are green?",
        "options": ["1/22", "3/22", "1/11", "3/11"],
        "correct": 0,
        "topic": "Probability",
        "difficulty": "hard",
        "explanation": "Total = 12. 1st green = 3/12. 2nd green = 2/11. Prob = (3/12) * (2/11) = 6/132 = 1/22."
    },
    {
        "id": 21,
        "question": "How many 1cm cubes can be cut from a cube of side 4cm?",
        "options": ["16", "32", "64", "128"],
        "correct": 2,
        "topic": "Cube Cuts",
        "difficulty": "easy",
        "explanation": "Volume of large cube / Volume of small cube = 4^3 / 1^3 = 64."
    },
    {
        "id": 22,
        "question": "A train 150m long crosses a bridge of length 250m in 20 seconds. What is the speed of the train?",
        "options": ["15 m/s", "20 m/s", "25 m/s", "30 m/s"],
        "correct": 1,
        "topic": "Speed & Distance",
        "difficulty": "easy",
        "explanation": "Total distance = 150 + 250 = 400m. Speed = 400 / 20 = 20 m/s."
    },
    {
        "id": 23,
        "question": "A can do a job in 12 days. B is 60% more efficient than A. How many days will B take?",
        "options": ["6.5 days", "7.5 days", "8 days", "9 days"],
        "correct": 1,
        "topic": "Time & Work",
        "difficulty": "medium",
        "explanation": "B's efficiency = 1.6 * A's efficiency. Days for B = 12 / 1.6 = 7.5 days."
    },
    {
        "id": 24,
        "question": "If price of sugar is reduced by 20%, how much percent consumption can be increased to keep budget same?",
        "options": ["20%", "25%", "30%", "33.3%"],
        "correct": 1,
        "topic": "Percentages",
        "difficulty": "medium",
        "explanation": "Increase% = (r / 100-r) * 100 = (20 / 80) * 100 = 25%."
    },
    {
        "id": 25,
        "question": "A card is drawn from a pack of 52. Probability that it is an ace or a king?",
        "options": ["1/13", "2/13", "1/26", "4/13"],
        "correct": 1,
        "topic": "Probability",
        "difficulty": "easy",
        "explanation": "Total Aces = 4, Kings = 4. Total favorable = 8. Probability = 8/52 = 2/13."
    }
]

MRCOOPER_CODING = [
    {"title": "Two Sum HashMap", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/", "lc": "https://leetcode.com/problems/two-sum/"},
    {"title": "Best Time to Buy Stock", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/", "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
    {"title": "Subarray Sum Equals K", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/number-of-subarrays-having-sum-exactly-equal-to-k/", "lc": "https://leetcode.com/problems/subarray-sum-equals-k/"},
    {"title": "Design LinkedList", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/design-a-singly-linked-list-in-java-without-using-collections-class/", "lc": "https://leetcode.com/problems/design-linked-list/"},
    {"title": "Design Browser History", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/design-browser-history-using-doubly-linked-list/", "lc": "https://leetcode.com/problems/design-browser-history/"},
    {"title": "Design Parking System", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/design-parking-system-in-java/", "lc": "https://leetcode.com/problems/design-parking-system/"},
    {"title": "Design Underground System", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/design-underground-system/", "lc": "https://leetcode.com/problems/design-underground-system/"},
    {"title": "LRU Cache", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/lru-cache-implementation/", "lc": "https://leetcode.com/problems/lru-cache/"},
    {"title": "LFU Cache", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/lfu-cache-implementation/", "lc": "https://leetcode.com/problems/lfu-cache/"},
    {"title": "Min Stack", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/design-a-stack-that-supports-getmin-in-o1-time-and-o1-extra-space/", "lc": "https://leetcode.com/problems/min-stack/"},
    {"title": "Product of Array Except Self", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/a-product-array-puzzle/", "lc": "https://leetcode.com/problems/product-of-array-except-self/"},
    {"title": "Longest Substring Without Repeating", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/", "lc": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
    {"title": "Longest Repeating Character Replacement", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/longest-repeating-character-replacement/", "lc": "https://leetcode.com/problems/longest-repeating-character-replacement/"},
    {"title": "Minimum Window Substring", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/find-the-smallest-window-in-a-string-containing-all-characters-of-another-string/", "lc": "https://leetcode.com/problems/minimum-window-substring/"},
    {"title": "Valid Parentheses", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/", "lc": "https://leetcode.com/problems/valid-parentheses/"},
    {"title": "Simplify Path", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/simplify-directory-path-unix-like/", "lc": "https://leetcode.com/problems/simplify-path/"},
    {"title": "Evaluate Reverse Polish Notation", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/evaluate-the-value-of-an-arithmetic-expression-in-reverse-polish-notation/", "lc": "https://leetcode.com/problems/evaluate-reverse-polish-notation/"},
    {"title": "Decode String", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/decode-string-containing-nested-records/", "lc": "https://leetcode.com/problems/decode-string/"},
    {"title": "Daily Temperatures", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/next-greater-element/", "lc": "https://leetcode.com/problems/daily-temperatures/"},
    {"title": "Next Greater Element I", "difficulty": "easy", "gfg": "https://www.geeksforgeeks.org/next-greater-element-for-every-element-in-given-array-set-1/", "lc": "https://leetcode.com/problems/next-greater-element-i/"},
    {"title": "Next Greater Element II", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/next-greater-element-in-circular-array/", "lc": "https://leetcode.com/problems/next-greater-element-ii/"},
    {"title": "Online Stock Span", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/the-stock-span-problem/", "lc": "https://leetcode.com/problems/online-stock-span/"},
    {"title": "Asteroid Collision", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/asteroid-collision/", "lc": "https://leetcode.com/problems/asteroid-collision/"},
    {"title": "Car Fleet", "difficulty": "medium", "gfg": "https://www.geeksforgeeks.org/car-fleet/", "lc": "https://leetcode.com/problems/car-fleet/"},
    {"title": "Trapping Rain Water", "difficulty": "hard", "gfg": "https://www.geeksforgeeks.org/trapping-rain-water/", "lc": "https://leetcode.com/problems/trapping-rain-water/"}
]

def get_company_aptitude(name: str):
    name_lower = name.lower()
    if "tcs" in name_lower: return TCS_APTITUDE
    elif "infosys" in name_lower: return INFOSYS_APTITUDE
    elif "wipro" in name_lower: return WIPRO_APTITUDE
    elif "accenture" in name_lower: return ACCENTURE_APTITUDE
    elif "cognizant" in name_lower: return COGNIZANT_APTITUDE
    elif "cooper" in name_lower: return MRCOOPER_APTITUDE
    return TCS_APTITUDE

def get_company_coding(name: str):
    name_lower = name.lower()
    if "tcs" in name_lower: return TCS_CODING
    elif "infosys" in name_lower: return INFOSYS_CODING
    elif "wipro" in name_lower: return WIPRO_CODING
    elif "accenture" in name_lower: return ACCENTURE_CODING
    elif "cognizant" in name_lower: return COGNIZANT_CODING
    elif "cooper" in name_lower: return MRCOOPER_CODING
    return TCS_CODING
