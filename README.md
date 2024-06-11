# fghi: Fiendish Grids of Hanzi by Ice

## Grids

- **Hanzigong:** [汉字宫](https://baike.baidu.com/item/汉字宫) is a series of 720 short videos teaching ~3000 Chinese characters. These were once popular in Thailand.
  - The first 47 episodes cover basic character components, as well as how complex characters are formed.
  - Afterwards, the more complex characters are grouped based on their "cores" (usually the phonetic parts but not always; e.g., 日: 旦昌旭时间晶旧...), and then the groups are arranged into themes (e.g., 日 is grouped with 月夕气云雨...).
  - Note that many common characters like 对, 再, and 年 are missing.
  - The grid was manually transcribed by me.
- **Ice's Grid:** My attempt to mimic the Hanzigong grouping with all common characters.
  - I aim to at least cover all HSK 1-6 characters. I also want to cover HSK 7 and the 3500 characters deemed in frequent use from the [Table of General Standard Chinese Characters (通用规范汉字表)](https://en.wikipedia.org/wiki/Table_of_General_Standard_Chinese_Characters).
  - This is work in progress and changes are to be expected.
- **Gold Book:** [汉字图解字典](https://baike.baidu.com/item/汉字图解字典/5068750) is a character dictionary that shows illustrations of character origins and (re-)analyzes them.
  - The characters are grouped by semantics. Related characters are further grouped together.
  - The grid was manually transcribed by me.
- **HSK Level (2021):** The list of characters from the [Chinese Proficiency Test version 3.0](http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202103/t20210329_523304.html).
  - The data comes from [Pleco's OCR'ed lists](https://github.com/elkmovie/hsk30) ([Forum post](https://plecoforums.com/threads/hsk-3-0-flashcards.6706/)).
- **Frequency (book):** [Jun Da](https://lingua.mtsu.edu/chinese-computing/statistics/)'s character frequency in modern Chinese text, up to rank 3000.
- **Frequency (movie):** Character frequency in movie subtitles from [SUBTLEX-CH](http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-ch), up to rank 3000.

## Filters

The characters outside the selected group will be grayed out.

- **HSK ?:** The list of characters from the [Chinese Proficiency Test](https://github.com/elkmovie/hsk30), up to the specified level.
- **Top ?000 (???):** The top-?000 characters from [Jun Da's list](https://lingua.mtsu.edu/chinese-computing/statistics/) (book texts) or [SUBTLEX-CH](http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-ch) (movie subtitles).
- **Official ??? ???:** Characters from the [Table of General Standard Chinese Characters (通用规范汉字表)](https://en.wikipedia.org/wiki/Table_of_General_Standard_Chinese_Characters). The data comes from [Wikisource](https://zh.wikisource.org/wiki/通用规范汉字表).

## Character Information and Vocabulary

When a character in the grid is clicked, the character's information and vocabulary entries will appear in the right pane.

- The character SVG comes from [makemeahanzi](https://github.com/skishore/makemeahanzi).
- The character meaning comes from the [Unihan Database](https://www.unicode.org/charts/unihan.html).
- The vocabulary entries come from several sources:
  - The [Chinese Proficiency Test](https://github.com/elkmovie/hsk30). These are marked with the HSK level (7 means 7-9, the unified advanced level).
  - [SUBTLEX-CH](http://crr.ugent.be/programs-data/subtitle-frequencies/subtlex-ch) (movie subtitles) and [BLCU Chinese Corpus](https://www.plecoforums.com/threads/word-frequency-list-based-on-a-15-billion-character-corpus-bcc-blcu-chinese-corpus.5859/). The lists are unified based on the word frequency rate.
    - A word is marked "c" if its frequency is more than 5 per million words; otherwise it is marked "x".
    - The "x" words will only be added until there are at least 3 words for the characters.
- The pronunciations and meanings come from [CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cc-cedict).
  - Words not found in CC-CEDICT are marked "???".
- Clicking on a character in a vocabulary entry will scroll the grid to that character.

## Other Attributions

- [Kanji Database Project](http://kanji-database.sourceforge.net/): Character information and decomposition
- [peterolson/chinese-lexicon](https://github.com/peterolson/chinese-lexicon/): Characters and words by the [Dong Chinese](https://www.dong-chinese.com) team
- [Multi-function Chinese Character Database](http://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/): Detailed and pretty reliable character origins
- [The Outlier Dictionary of Chinese Characters](https://www.outlier-linguistics.com/collections/chinese/products/outlier-dictionary-of-chinese-characters): Reliable character origins
