document.addEventListener("DOMContentLoaded", () => {

    let seats = document.querySelectorAll(".seat_select");
    const bookBtn = document.querySelector("#book-btn");

    // context from djngo 
    let moviedata = document.querySelector("#movie-data")
    let bookedSeatsIndices = moviedata.dataset.list.split(",").map(Number)
    let fakeData = document.querySelector("#facebooking")
    let  fakeBooking = fakeData.dataset.list.split(",").map(Number)
    let limit = 6
    let bookedSeatsIndex =Array();
    let selectSeatCount = 0;
    let selectSeatIndices = [];

    // geting data from localstorage
    // let data = JSON.parse(localStorage.getItem("bookedSeatsIndex"));
    bookedSeatsIndex = bookedSeatsIndex.concat(bookedSeatsIndices)

    // booking seats
    bookSeats = (list) => {
        if (list) {
            for (const index of list) {
                    seats[index].classList.remove("seat_selected");
                    seats[index].classList.toggle("seats-booked");
            }
        }
    };
    fakeSeatsBook = (list) => {
        if (list) {
            for (const index of list) {
                if(!bookedSeatsIndices.includes(index)){
                    seats[index].classList.remove("seat_selected");
                    seats[index].classList.toggle("seats-booked");   
                }
            }
        }
    };
    window.addEventListener("load",()=>{
        bookSeats(bookedSeatsIndices)
        fakeSeatsBook(fakeBooking)
    })

    // showing seats number on window
    // count = 1
    let showingSeatNumber = (data)=>{
        data.forEach((ele,ind)=>{
            seats[ind].textContent= ind + 1 
        })
    }

    //cal how many seat to be selected 
    const calSeatsCount = () => {
        const selectSeatLenght = document.querySelectorAll(".seat_selected")
        return selectSeatLenght.length;
    };

    // selecting seats 
    count  = 1
    const selectSeats = (ele, index) => {
        
        if (selectSeatCount < limit ) {
            if (!( bookedSeatsIndex.includes(index) && fakeBooking.includes(index))){
                if (!selectSeatIndices.includes(index)) {
                    selectSeatIndices.push(index);
                    ele.classList.toggle("seat_selected");
                } else {
                    const indexToRemove = selectSeatIndices.indexOf(index);
                    ele.classList.remove("seat_selected");
                    if (indexToRemove !== -1) {
                        selectSeatIndices.splice(indexToRemove, 1);
                    }
                }
            }
            // console.log(selectSeatIndices);
        } else {
            ele.classList.remove("seat_selected");
        }
        selectSeatCount = calSeatsCount();
    };

    // clicking on seats for booking 
    seats.forEach((seat, index) => {
        if (!bookedSeatsIndex.includes(index)) {
            seat.addEventListener("click", (e) => {
                e.preventDefault();
                selectSeats(seat, index);
            });
        }
    });

    // to purchase the movie tickets
    bookBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if(selectSeatIndices.length >= 1){
            if(confirm("book the seat")){
                bookSeats(selectSeatIndices);
                bookedSeatsIndex = [...bookedSeatsIndex,...selectSeatIndices];
                selectSeatIndices = [];
                window.location.reload
            }
        }

    // Send booked seat data to the server
    $(document).on("click","#book-btn",()=>{
        $.ajax({
            type:"POST",
            url:window.location.href,
            data:{
                "booked_seats": JSON.stringify(bookedSeatsIndex),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                "name":"murali"
            },
            success:()=>{
                console.log("done");
            },
            error:()=>{
                console.log("error");
            }
    
        })
    })
});
 
});
