$(function () {

  function gup(name) {
    let regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
    let results = regex.exec(window.location.href);
    return results === null ? "" : decodeURIComponent(results[1]);
  }

  /** Generate a tag in SVG namespace */
  function S(tag, attr) {
    return $(document.createElementNS(
      "http://www.w3.org/2000/svg", tag.replace(/[<>]/g, '')))
      .attr(attr || {});
  }

  $('#toolbar').append('Display up to HSK ');
  [1, 2, 3, 4, 5, 6, 'C', 'all'].forEach(function (level) {
    $('<button>').attr('id', 'btn-' + level).text(level).click(function () {
      $('#wrapper').removeClass().addClass('d' + level);
      $('#toolbar button').removeClass();
      $(this).addClass('selected');
    }).appendTo('#toolbar');
  });
  $('#btn-all').click();

  let currentChar = null;

  function clearData(unknownChar) {
    if (unknownChar !== currentChar) return;
    $('#words-pane').empty();
    $('<div class=char-info>').appendTo('#words-pane')
      .append('Character ' + unknownChar + ' not found!');
  }

  function createWordEntry(parentDiv, cat, word, level, pron, gloss) {
    let levelText = {
      'char': '',
      'word': level,
      'extraWord': 'x',
    }[cat];
    let wordDiv = (
      $('<div>')
        .append($('<span class=level>').text(levelText))
        .append(genWordSpan(word))
        .append($('<span class=pron>').text(pron))
        .append($('<div class=gloss>').text(gloss))
        .appendTo(parentDiv)
    );
    if (levelText !== '') {
      wordDiv.addClass('h' + levelText);
    }
  }

  function populateData(charData) {
    if (charData.char !== currentChar) return;
    $('#words-pane').empty();
    // char
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
    createWordEntry(wordsList, 'char', charData.char, null, charData.info.pron,
      'Char Meanings: ' + charData.info.gloss);
    charData.words.forEach(function (entry) {
      // Simp, Level, Pron, Gloss
      createWordEntry(wordsList, 'word', entry[0], entry[1], entry[2], entry[3]);
    });
    charData.extraWords.forEach(function (entry) {
      // Simp, Level, Pron, Gloss
      createWordEntry(wordsList, 'extraWord', entry[0], entry[1], entry[2], entry[3]);
    });
  }

  function genWordSpan(word) {
    let span = $('<span class=word>');
    for (let i = 0; i < word.length; i++) {
      $('<span class=wc>').text(word.charAt(i)).appendTo(span);
    }
    return span;
  }

  let charToTd = {};

  function generate(grid_raw, hsk_raw) {
    let charToLevel = {}, commonChars = {};
    [1, 2, 3, 4, 5, 6].forEach(function (level) {
      let levelChars = hsk_raw[level];
      for (let i = 0; i < levelChars.length; i++) {
        charToLevel[levelChars[i]] = level;
      }
    });
    for (let i = 0; i < hsk_raw['C'].length; i++) {
      commonChars[hsk_raw['C'][i]] = true;
    }
    // Create the grid
    let grid = $('<table>').appendTo('#chars-pane');
    grid_raw.forEach(function (row_raw) {
      let row = $('<tr>').appendTo(grid);
      $('<th>').text(row_raw[0]).appendTo(row);
      for (let i = 0; i < row_raw[1].length; i++) {
        let x = row_raw[1].charAt(i);
        charToTd[x] = $('<td>').text(x).appendTo(row);
        if (charToLevel[x] !== undefined)
          charToTd[x].addClass('h' + charToLevel[x]);
        else
          charToTd[x].addClass('hx');
        if (commonChars[x] === undefined)
          charToTd[x].addClass('hC');
      }
    });
    grid.on('click', 'td', function (event) {
      let cell = $(this), char = cell.text(), code = char.charCodeAt(0);
      $('#chars-pane .selected').removeClass('selected');
      cell.addClass('selected');
      currentChar = char;
      $.get('data/vocab/' + code + '.json', populateData).fail(function () {
        clearData(char);
      });
    });
  }

  $('#words-pane').on('click', '.wc', function () {
    let td = charToTd[$(this).text()];
    if (!td) return;
    $('#chars-pane').animate({ scrollTop: td.position().top });
    td.addClass('flash');
    setTimeout(function () { td.removeClass('flash'); }, 1000);
  });

  let gridName = gup('grid') || 'fghi';
  $.get('data/grid-' + gridName + '.json', function (grid_raw) {
    $.get('data/hsk.json', function (hsk_raw) {
      generate(grid_raw, hsk_raw);
    });
  });

});
