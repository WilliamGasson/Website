
  //Make the DIV element draggagle:
  blackPieces = ["bQ","bK","bR1","bN1","bB1","bR2","bN2","bB2","bP1","bP2","bP3","bP4","bP5","bP6","bP7","bP8", ]
  whitePieces = ["wQ","wK","wR1","wN1","wB1","wR2","wN2","wB2","wP1","wP2","wP3","wP4","wP5","wP6","wP7","wP8" ]

  for (let i = 0; i < blackPieces.length; i++) {
    dragElement(document.getElementById(blackPieces[i]));
  }
  for (let i = 0; i < whitePieces.length; i++) {
    dragElement(document.getElementById(whitePieces[i]));
  }
  
  function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    var piece=0,  top =0, left=0,  col=0, row=0;
    var myJSON = [];
    if (document.getElementById(elmnt.id + "header")) {
        /* if present, the header is where you move the DIV from:*/
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } 
    else {
        /* otherwise, move the DIV from anywhere inside the DIV:*/
        elmnt.onmousedown = dragMouseDown;
    }
      
    function dragMouseDown(e) {
      console.log(1)

      e = e || window.event;
      e.preventDefault();
      // get the mouse cursor position at startup:
      pos3 = e.clientX;
      pos4 = e.clientY;

      document.onmouseup = closeDragElement;

      // call a function whenever the cursor moves:
      document.onmousemove = elementDrag;
      piece = elmnt.id;

      pieceDetails()
      console.log(myJSON)

    }
      
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      // set the element's new position:
      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";

    }

    function pieceDetails(e) {

      top = (elmnt.offsetTop - pos2)+40;
      left = (elmnt.offsetLeft - pos1)+40;

      // col = ["a","b","c","d","e","f","g","h"]
      // row = ["1","2","3","4","5","6","7","8"]
      // col[int(left/100)]
      // row[int(top/100)]

      if (left > 0 && left <= 100) {
        col = "a";
      } else if (left > 100 && left <= 200) {
        col = "b";
      } else if (left > 200 && left <= 300) {
        col = "c";
      } else if (left > 300 && left <= 400) {
        col = "d";
      } else if (left > 400 && left <= 500) {
        col = "e";
      } else if (left > 500 && left <= 600) {
        col = "f";
      } else if (left > 600 && left <= 700) {
        col = "g";
      } else if (left > 700 && left <= 800) {
        col = "h";
      }
      
      if (top > 0 && top < 100) {
        row = "8";
      } else if (top > 100 && top <= 200) {
        row = "7";
      } else if (top > 200 && top <= 300) {
        row = "6";
      } else if (top > 300 && top <= 400) {
        row = "5";
      } else if (top > 400 && top <= 500) {
        row = "4";
      } else if (top > 500 && top <= 600) {
        row = "3";
      } else if (top > 600 && top <= 700) {
        row = "2";
      } else if (top > 700 && top <= 800) {
        row = "1";
      }

      document.getElementById("top").innerHTML = top;
      document.getElementById("left").innerHTML = left;
      document.getElementById("piece").innerHTML = piece;
      document.getElementById("col").innerHTML = col;
      document.getElementById("row").innerHTML = row;

      const obj = {piece: piece, row: row, col: col};
      myJSON = JSON.stringify(obj);
    }
    
    function closeDragElement() {
      /* stop moving when mouse button is released:*/
      console.log(2)
      pieceDetails()
      console.log(myJSON)
      postPosition()
      document.onmouseup = null;
      document.onmousemove = null;
    }
    function postPosition() {
      $.ajax({
          type: "POST",
          url: "{{ url_for('chess') }}",
          data: {"move" : myJSON },
      })
  }
  }


  



