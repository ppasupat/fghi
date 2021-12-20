$(function () {
  'use strict';

  // ################################################
  // Utilities

  function gup(name) {
    let regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
    let results = regex.exec(window.location.href);
    return results === null ? "" : decodeURIComponent(results[1]);
  }

  function scrollOffset(cell) {
    return cell.position().top - $('#chars-pane-inner').position().top - $('body').height() * .4;
  }

  // Generate a tag in SVG namespace
  function S(tag, attr) {
    return $(document.createElementNS(
      'http://www.w3.org/2000/svg', tag.replace(/[<>]/g, '')))
      .attr(attr || {});
  }

  // ################################################
  // Character information

  // Minimum word frequency (per million) to be counted as "common"
  const MIN_FREQ = 5.0;

  let currentChar = null;

  function clearData(unknownChar) {
    if (unknownChar !== currentChar) return;
    $('#words-pane').empty();
    $('<div class=char-info>').appendTo('#words-pane')
      .append('Character ' + unknownChar + ' not found!');
    $('#words-pane').scrollTop(0);
  }

  function createWordEntry(parentDiv, word, level, pron, gloss) {
    let wordSpan = $('<span class=word>');
    for (let i = 0; i < word.length; i++) {
      $('<span class=wc>').text(word.charAt(i)).appendTo(wordSpan);
    }
    let wordDiv = (
      $('<div class=entry>')
        .append($('<p>')
          .append($('<span class=level>').text(level))
          .append(wordSpan)
          .append($('<span class=pron>').text(pron)))
        .append($('<p class=gloss>').text(gloss))
        .appendTo(parentDiv)
    );
    if (level !== '') {
      wordDiv.addClass('v' + level);
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
      // Simp, Freq, Pron, Gloss
      let level = entry[1] >= MIN_FREQ ? 'c' : 'x';
      createWordEntry(wordsList, entry[0], level, entry[2], entry[3]);
    });
    $('#words-pane').scrollTop(0);
  }

  // ################################################
  // Character grid

  // Maximum character frequency for the filters
  const CHAR_FREQ1 = 1000, CHAR_FREQ2 = 2000;

  let charToCats = null, charToCell = {};

  function readCats(catsRaw) {
    if (charToCats !== null) throw 'readCats already called.';
    charToCats = {};
    for (let cat of Object.keys(catsRaw)) {
      for (let i = 0; i < catsRaw[cat].length; i++) {
        let char = catsRaw[cat][i], catName = cat;
        if (cat === 'B' || cat === 'M') {
          if (i >= CHAR_FREQ1) {
            if (i >= CHAR_FREQ2) continue;
            catName += '2';
          }
        }
        if (charToCats[char] === undefined) {
          charToCats[char] = [];
        }
        charToCats[char].push(catName);
      }
    }
  }

  function genSection() {
    return $('<div class=grid-section>').appendTo('#chars-pane-inner');
  }

  function populateGrid(gridRaw) {
    $('#chars-pane-inner').empty();
    let currentSection = null;
    gridRaw.forEach(function (row_raw) {
      if (row_raw.length === 0) return;
      if (row_raw[0] === '#') {
        // Start a new section
        currentSection = genSection();
        if (row_raw.length > 1) {
          $('<p class=grid-section-title>').text(row_raw[1]).appendTo(currentSection);
        }
      } else {
        // A line of characters = alternate between annotations and characters
        if (currentSection === null) currentSection = genSection();
        let row = $('<p>').appendTo(currentSection);
        for (let i = 0; i < row_raw.length; i++) {
          if (i % 2 == 0) {
            if (Array.isArray(row_raw[i])) {
              row_raw[i].forEach(function (x) {
                $('<b>').text(x).appendTo(row);
              });
            } else if (row_raw[i] !== '') {
              $('<b>').text(row_raw[i]).appendTo(row);
            }
          } else {
            for (let x of row_raw[i]) {
              charToCell[x] = $('<i>').text(x).appendTo(row);
              (charToCats[x] || []).forEach(function (cat) {
                charToCell[x].addClass('h' + cat);
              });
            }
          }
        }
      }
    });
    $('#chars-pane').scrollTop(0);
  }

  // Click on a character in the grid
  $('#chars-pane').on('click', 'i', function (event) {
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
    let cell = charToCell[$(this).text()];
    if (!cell) return;
    $('#chars-pane').animate({ scrollTop: scrollOffset(cell) });
    cell.addClass('flash');
    setTimeout(function () { cell.removeClass('flash'); }, 1000);
  });

  // The "Grid:" dropdown
  function changeGrid() {
    $('#grid-select').prop('disabled', true);
    $.get('data/grids/grid-' + $('#grid-select').val() + '.json', function (gridRaw) {
      populateGrid(gridRaw);
      changeFilter();
      $('#grid-select').prop('disabled', false);
    });
  }
  $('#grid-select').change(changeGrid);

  // The "Show:" dropdown
  function changeFilter() {
    let name = $('#show-select').val();
    $('#chars-pane').removeClass().addClass('f-' + name);
  }
  $('#show-select').change(changeFilter);

  // ################################################
  // Start!

  $('#grid-select').val(gup('grid') || 'hsk');
  $.get('data/cats.json', function (catsRaw) {
    readCats(catsRaw);
    changeGrid();
  });

});
