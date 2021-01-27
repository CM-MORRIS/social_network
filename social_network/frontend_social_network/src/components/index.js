import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// Props: are variables passed to it by its parent component. 
// State: is still variables, but directly initialized and managed by the component.

// class Square extends React.Component {

//     /*
//         In JavaScript classes, you need to always 
//         call super when defining the constructor of a subclass. 
//         All React component classes that have a constructor 
//         should start with a super(props) call.
//      */
//     // constructor(props) {
//     //     super(props);
//     //     this.state = {
//     //         value: null,
//     //     };
//     // }

//     render() {
//         return (
//             <button
//                 className="square"

//                 // onClick function provided by the Board 

//                 // event listener -> calls props.onClick <- specified by Board
//                 onClick={ () => this.props.onClick() }
//             >
//                 { this.props.val }
//             </button>
//         );
//     }
// }

/*
    function components are a simpler way to write components 
    that only contain a render method and don’t have their own state. 
    Instead of defining a class which extends React.Component, 
    can write a function that takes props as input and returns what should be rendered. 
 */
function Square(props) {
    return (
        <button className="square" onClick={props.onClick}>
            { props.val } 
        </button>
    )
}

class Board extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            isXNext: true,
        };
    }

    // .slice to create copy of the array to change - not mutating data directly
    handleClick(i) {
        const squares = this.state.squares.slice();

        // if winner or square is occupied return
        if (calculateWinner(squares) || squares[i]) {
            return;
        }

        const player = this.state.isXNext ? 'X' : 'O';
        squares[i] = player;
        this.setState({
            squares: squares, 
            isXNext: !this.state.isXNext,
        });
    }

    renderSquare(i) {
        return (
            <Square val={this.state.squares[i]}
                // Board passes this to square, so square calls 'this.handleClick(i)' when clicked
                onClick={() => this.handleClick(i)}
            />
        );
    }

    render() {

        const winner = calculateWinner(this.state.squares);
        let status;

        if (winner) {
          status = 'Winner: ' + winner;
        } 
        else {
          status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
        }
    

        return (
            <div>
                <div className="status">{status}</div>
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}

class Game extends React.Component {

    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board />
                </div>
                <div className="game-info">
                    <div>{/* status */}</div>
                    <ol>{/* TODO */}</ol>
                </div>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Game />,
    document.getElementById('root')
);

/*
    Note

    The DOM <button> element’s onClick attribute has a special meaning 
    to React because it is a built-in component. 
    For custom components like Square, the naming is up to you. 
    We could give any name to the Square’s onClick prop 
    or Board’s handleClick method, 
    and the code would work the same. 
    In React, it’s conventional to use on[Event] names for props
    and handle[Event] for the methods which handle the events.
 */


function calculateWinner(squares) {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];

    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines[i];
        if (squares[a] === squares[b] && squares[a] === squares[c]) {
            return squares[a];
        }
    }
    return null;
}