/**
 * Created by user on 02.04.16.
 */

function Puzzle() {
    var matrix = [];
    var width = 4;
    var heigth = 4;
    var elem = ' ';
    var coord = null;


    function matrix_generator() {
        for (var i = 0; i < heigth; i++) {
            var row = [];
            for (var j = 0; j < width; j++) {
                row.push(j + 1 + width * i);
            }
            matrix.push(row);
        }
        matrix[width - 1][heigth - 1] = elem;
        return matrix
    }

    function print_board() {
        var parent = document.getElementsByClassName("parent")[0];
        var new_parent = document.createElement('div');
        new_parent.className = 'parent';

        for (var i = 0; i < matrix.length; i++) {
            var row = document.createElement('div');
            row.className = "row ";

            for (var j = 0; j < matrix[i].length; j++) {
                var field = document.createElement('div');
                field.className = "field " + i;
                field.textContent = matrix[i][j];
                row.appendChild(field);
            }
            new_parent.appendChild(row);
        }
        parent.outerHTML = new_parent.outerHTML;
    }

    function find_coord() {
        var x = null;
        var y = null;
        for (var i = 0; i < matrix.length; i++) {
            y = i;
            for (var j = 0; j < matrix[i].length; j++) {
                if (matrix[i][j] == elem) {
                    x = j;
                    return {"x": x, "y": y};
                }
            }
        }
    }

    function perform_move(direction) {
        //var moves = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'};
        //if (moves[direction] != undefined) {
        //    console.log(direction);
        coord = find_coord();
        x = coord['x'];
        y = coord['y'];
        var ch = matrix[y][x];

        if (y > 0 && direction == 'w') {
            matrix[y][x] = matrix[y - 1][x];
            matrix[y - 1][x] = ch;
            return {'x': x, 'y': y - 1};
        }
        if (y < 3 && direction == 's') {
            matrix[y][x] = matrix[y + 1][x];
            matrix[y + 1][x] = ch;
            return {'x': x, 'y': y + 1}
        }
        if (x > 0 && direction == 'a') {
            matrix[y][x] = matrix[y][x - 1];
            matrix[y][x - 1] = ch;
            return {'x': x - 1, 'y': y}
        }
        if (x < 3 && direction == 'd') {
            matrix[y][x] = matrix[y][x + 1];
            matrix[y][x + 1] = ch;
            return {'x': x + 1, 'y': y}
        }
        return {"x": x, "y": y};
    }

    function get_choice() {
        document.onkeypress = function (event) {
            var char = String.fromCharCode(event.which);
            coord = perform_move(char);
            print_board();
        }
    }

    function shuffle() {
        var choices = ['w', 's', 'd', 'a']
        for (var i = 0; i < 999; i++) {
            var min = 0;
            var max = 3;
            var ch = Math.floor(Math.random() * (max - min + 1)) + min;
            perform_move(choices[ch]);
        }
    }

    this.run = function () {
        console.log('hello');
        matrix = matrix_generator();
        coord = find_coord();
        console.log(coord);
        shuffle();
        print_board();
        get_choice();
    };

}
window.onload = function () {
    var game = new Puzzle();
    game.run();
};
