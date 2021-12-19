$(function () {
  "use strict";

  // ################################################
  // Utilities

  // Generate a tag in SVG namespace
  function S(tag, attr) {
    return $(document.createElementNS(
      "http://www.w3.org/2000/svg", tag.replace(/[<>]/g, '')))
      .attr(attr || {});
  }

  // ################################################
  // Character information

  let currentChar = null;

  function clearData(unknownChar) {
    if (unknownChar !== currentChar) return;
    $('#words-pane').empty();
    $('<div class=char-info>').appendTo('#words-pane')
      .append('Character ' + unknownChar + ' not found!');
  }

  function createWordEntry(parentDiv, word, level, pron, gloss) {
    let wordSpan = $('<span class=word>');
    for (let i = 0; i < word.length; i++) {
      $('<span class=wc>').text(word.charAt(i)).appendTo(wordSpan);
    }
    let wordDiv = (
      $('<div>')
        .append($('<span class=level>').text(level))
        .append(wordSpan)
        .append($('<span class=pron>').text(pron))
        .append($('<div class=gloss>').text(gloss))
        .appendTo(parentDiv)
    );
    if (level !== '') {
      wordDiv.addClass('h' + level);
    }
  }

  function populateCharData(charData) {
    if (charData.char !== currentChar) return;
    $('#words-pane').empty();
    // character
    let charInfoBox = $('<div class=char-info>').appendTo('#words-pane');
    let svg = $('<svg class=char-img>').attr({
      'width': 256, 'height': 256,
    }).appendTo(charInfoBox);
    let svgOuterGroup = S('g', {
      'transform': 'scale(.25)',
    }).appendTo(svg);
    let svgGroup = S('g', {
      'transform': 'scale(1, -1) translate(0, -900)',
    }).appendTo(svgOuterGroup);
    charData.strokes.forEach(function (d, i) {
      S('path', {'d': d}).appendTo(svgGroup);
    });
    // words
    let wordsList = $('<div class=words-list>').appendTo('#words-pane');
    createWordEntry(wordsList, charData.char, '', charData.info.pron,
      'Char Meanings: ' + charData.info.gloss);
    charData.words.forEach(function (entry) {
      // Simp, Level, Pron, Gloss
      createWordEntry(wordsList, entry[0], entry[1], entry[2], entry[3]);
    });
    charData.extraWords.forEach(function (entry) {
      // Simp, Freq (ignored), Pron, Gloss
      createWordEntry(wordsList, entry[0], 'x', entry[2], entry[3]);
    });
  }

  // ################################################
  // Character grid

  let charToCats = null, charToTd = {};

  function readCats(catsRaw) {
    if (charToCats !== null) throw 'readCats already called.';
    charToCats = {};
    for (let cat of Object.keys(catsRaw)) {
      for (let char of catsRaw[cat]) {
        if (charToCats[char] === undefined) {
          charToCats[char] = [];
        }
        charToCats[char].push(cat);
      }
    }
  }

  function populateGrid(gridRaw) {
    charToTd = {};
    $('#chars-pane').empty();
    let grid = $('<table>').appendTo('#chars-pane');
    gridRaw.forEach(function (row_raw) {
      let row = $('<tr>').appendTo(grid);
      $('<th>').text(row_raw[0]).appendTo(row);
      for (let x of row_raw[1]) {
        charToTd[x] = $('<td>').text(x).appendTo(row);
        let isCommon = false;
        (charToCats[x] || []).forEach(function (cat) {
          if (cat === 'C') {
            isCommon = true;
          } else {
            charToTd[x].addClass('h' + cat);
          }
        });
        if (!isCommon) charToTd[x].addClass('hUC');
      }
    });
  }

  // Click on a character in the grid
  $('#chars-pane').on('click', 'td', function (event) {
    let cell = $(this), char = cell.text(), code = char.charCodeAt(0);
    $('#chars-pane .selected').removeClass('selected');
    cell.addClass('selected');
    currentChar = char;
    $.get('data/vocab/' + code + '.json', populateCharData).fail(function () {
      clearData(char);
    });
  });

  // Click on a character in a vocab entry
  $('#words-pane').on('click', '.wc', function () {
    let td = charToTd[$(this).text()];
    if (!td) return;
    $('#chars-pane').animate({ scrollTop: td.position().top });
    td.addClass('flash');
    setTimeout(function () { td.removeClass('flash'); }, 1000);
  });

  // The "Show:" dropdown
  function changeFilter() {
    let name = $('#show-select').val();
    $('#chars-pane').removeClass().addClass('f-' + name);
  }
  $('#show-select').change(changeFilter);

  $.get('data/cats.json', function (catsRaw) {
    readCats(catsRaw);
    $.get('data/grid-fghi.json', function (gridRaw) {
      populateGrid(gridRaw);
      changeFilter();
    });
  });

});
