/* =====================================
   JAKE'S PLUMBING WEBSITE JAVASCRIPT
===================================== */



document.addEventListener("DOMContentLoaded", function(){


    const bookingForm = document.querySelector(".booking form");


    if(bookingForm){


        bookingForm.addEventListener("submit", function(e){


            e.preventDefault();



            const name =
            document.querySelector('input[name="name"]').value;



            const phone =
            document.querySelector('input[name="phone"]').value;



            const time =
            document.querySelector('select[name="time"]').value;



            const service =
            document.querySelector('select[name="service"]').value;



            const message =
            document.querySelector('textarea[name="message"]').value;



            if(
                name === "" ||
                phone === ""
            ){

                alert(
                "Please fill in your name and phone number."
                );

                return;

            }



            saveReservation({

                name:name,

                phone:phone,

                time:time,

                service:service,

                message:message

            });



        });



    }



});









/* =====================================
   RESERVATION STORAGE
===================================== */


function saveReservation(data){



    let reservations = 
    JSON.parse(
    localStorage.getItem("reservations")
    )
    || [];




    const today =
    new Date().toDateString();




    const todaysReservations =
    reservations.filter(
        item => item.date === today
    );




    const slotCount =
    todaysReservations.filter(
        item => item.time === data.time
    ).length;





    /*
       Each slot can have maximum 3 reservations
       In production Flask will handle this securely
    */


    if(slotCount >= 3){


        alert(

        "Sorry, this time slot is fully booked. Please choose another time."

        );


        return;


    }






    data.date = today;



    reservations.push(data);



    localStorage.setItem(

        "reservations",

        JSON.stringify(reservations)

    );




    alert(

    "Your reservation request has been received. Jake's Plumbing will contact you soon."

    );




    document.querySelector(".booking form").reset();



}










/* =====================================
   SMOOTH SCROLL BUTTONS
===================================== */


const buttons =
document.querySelectorAll("a[href^='#']");



buttons.forEach(button=>{


    button.addEventListener(
    "click",
    function(e){


        const target =
        document.querySelector(
        this.getAttribute("href")
        );



        if(target){


            e.preventDefault();


            target.scrollIntoView({

                behavior:"smooth"

            });


        }


    });


});









/* =====================================
   SIMPLE IMAGE HOVER EFFECT
===================================== */


const images =
document.querySelectorAll(".service-card img");



images.forEach(img=>{


    img.addEventListener(
    "mouseenter",
    ()=>{


        img.style.filter =
        "brightness(85%)";


    });



    img.addEventListener(
    "mouseleave",
    ()=>{


        img.style.filter =
        "brightness(100%)";


    });



});
