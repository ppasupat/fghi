$(function () {

  $('#toolbar').append('Display up to HSK ');
  [1, 2, 3, 4, 5, 6, 'all'].forEach(function (level) {
    $('<button>').attr('id', 'btn-' + level).text(level).click(function () {
      $('#wrapper').removeClass().addClass('d' + level);
      $('#toolbar button').removeClass();
      $(this).addClass('selected');
    }).appendTo('#toolbar');
  });
  $('#btn-all').click();

  function generate(grid_raw, hsk_raw, vocab_raw) {
    var charToLevel = {};
    [1, 2, 3, 4, 5, 6].forEach(function (level) {
      var levelChars = hsk_raw[level];
      for (var i = 0; i < levelChars.length; i++) {
        charToLevel[levelChars[i]] = level;
      }
    });
    var grid = $('<table>').appendTo('#chars-pane');
    grid_raw.forEach(function (row_raw) {
      var row = $('<tr>').appendTo(grid);
      for (var i = 0; i < row_raw.length; i++) {
        var x = row_raw.charAt(i);
        row.append($('<td>').text(x).addClass('h' + charToLevel[x]));
      }
    });
    grid.on('click', 'td', function (event) {
      var cell = $(this), char = cell.text();
      $('#chars-pane .selected').removeClass('selected');
      cell.addClass('selected');
      $('#words-pane').empty();
      var wordsList = $('<div class=words-list>').appendTo('#words-pane');
      [1, 2, 3, 4, 5, 6].forEach(function (level) {
        vocab_raw[level].forEach(function (word) {
          var c = word.indexOf(char), p = word.indexOf('（');
          if (c != -1 && (p == -1 || c < p)) {
            wordsList.append(
              $('<div>').addClass('h' + level)
              .append($('<span class=level>').text(level))
              .append($('<span class=word>').text(word)));
          };
        });
      });
    });
  }

  $.get('data/grid.json', function (grid_raw) {
    $.get('data/hsk.json', function (hsk_raw) {
      $.get('data/vocab.json', function (vocab_raw) {
        generate(grid_raw, hsk_raw, vocab_raw);
      });
    });
  });

});
