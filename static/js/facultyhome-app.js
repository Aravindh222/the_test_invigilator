window.addEventListener('load',function(){

    var main = document.getElementById('maincontainer');
    document.getElementsByClassName('containers')[1].classList.add('makebigger');

    main.addEventListener('click',process);
    var containers = document.getElementsByClassName('containers');
    containers[0].style.background = '#3CB371';
    containers[1].style.background = '#DB7093';
    containers[2].style.background = '#DDA0DD';

    var freezeClic = false;

    document.addEventListener("click", e => {
        if (freezeClic) {
            e.stopPropagation();
            e.preventDefault();
        }
    }, true);
    

    function process(event){

        //calculate the boundary

        var containers = document.getElementsByClassName('containers');

        var left = containers[0];
        var right = containers[1];

        var left_bound = left.getBoundingClientRect();
        var right_bound = right.getBoundingClientRect();

        if(event.clientX >= right_bound.x && event.clientX <= (right_bound.x + right_bound.width)){
            if(event.clientY >= right_bound.y && event.clientY <= (right_bound.y + right_bound.height)){
                console.log("You clicked the middle");
                freezeClic = true;


                console.log(right_bound)
                // var middle_x = right_bound.x;
                // var middle_y = right_bound.y;
                // var middle_width = right_bound.width;
                // var middle_height = right_bound.height;

                var divtoinsert = document.createElement('div');
                divtoinsert.classList = right.classList;
                
                divtoinsert.style.background = right.style.background;
                divtoinsert.style.border = 'None';
                divtoinsert.style.color = 'white';
                var maindiv = document.getElementById('displayclass');

                document.querySelector('header').style.display = 'None';
                document.querySelector('.main-container').style.display = 'None';
                document.querySelector('.displayclass').style.display = 'flex';
                dup = right.textContent;
                right.textContent = '';

                maindiv.append(divtoinsert);
                
                console.log(divtoinsert.classList)

                setTimeout(()=>{
                    divtoinsert.classList.add('makefullscreen');
                },10)  
                
                setTimeout(()=>{
                     location.href = `${'facultyhomepage-' + dup.toLowerCase() + '.html'}`;
                },1000)

                setTimeout(function(){
                    freezeClic = false;
                },2000);
            }  
        }
        
        

        else if(event.clientX >= left_bound.x && event.clientX <= (left_bound.x + left_bound.width)){
            if(event.clientY >= left_bound.y && event.clientY <= (left_bound.y + left_bound.height)){
                console.log("you clicked the left");
                freezeClic = true;

                //shrink before doing shit.
                right.classList.remove('makebigger');


                //the shit
                setTimeout(function(){

                    left_bound = left.getBoundingClientRect();

                    var pos_left = left_bound;
                    var target_pos = right.getBoundingClientRect();


                    var i = target_pos.left - pos_left.left;


                    left.animate(
                        [
                            {transform: 'translateX(0)'},
                            {transform: 'translateX(' + i + 'px' + ')'},
                        ],
                        {
                            duration:300,
                            easing:'ease',
                            fill:"forwards",
                            iterations:1,
                            delay:0
                        }
                    );

                    i *= -1;

                    right.animate(
                        [
                            {transform: 'translateX(0)'},
                            {transform: 'translateX(' + i + 'px' + ')'},
                        ],
                        {
                            duration:300,
                            easing:'ease',
                            fill:"forwards",
                            iterations:1,
                            delay:0
                        }
                    );

                    var delayInMilliseconds = 600;
                    setTimeout(function() {

                        var c1 = document.createElement('div');
                        c1.classList.add('containers');
                        c1.textContent =containers[0].textContent;
                        c1.style.background = containers[0].style.background;
                        console.log(containers[0].style.background);
                        //c1.style.background = '#DB7093';
                        
                        var c2 = document.createElement('div');
                        c2.classList.add('containers');
                        c2.textContent =containers[1].textContent;
                        c2.style.background = containers[1].style.background;
                        console.log(containers[1].style.background);
                        // c2.style.background = '#3CB371';
            
                        var c3 = document.createElement('div');
                        c3.classList.add('containers');
                        c3.textContent =containers[2].textContent;
                        console.log(containers[2].style.background);
                        c3.style.background = containers[2].style.background;
            
                        main.innerHTML = '';
                        main.appendChild(c2);
                        main.appendChild(c1);
                        main.appendChild(c3);

                        setTimeout(function(){
                            document.getElementsByClassName('containers')[1].classList.add('makebigger');
                        },100);

                        
                    }, delayInMilliseconds);
                },600);

                setTimeout(function(){
                    freezeClic = false;
                },2000);
            }
        }

        else{
            var left = containers[2];
            var right = containers[1];

            var left_bound = left.getBoundingClientRect();
            
            if(event.clientX >= left_bound.x && event.clientX <= (left_bound.x + left_bound.width)){
                if(event.clientY >= left_bound.y && event.clientY <= (left_bound.y + left_bound.height)){

                    console.log("you clicked the right");

                    freezeClic = true;
                    //shrink before doing shit.

                    right.classList.remove('makebigger');

                    //the shit
                    setTimeout(function(){

                        left_bound = left.getBoundingClientRect();

                        var pos_left = left_bound;
                        var target_pos = right.getBoundingClientRect();


                        var i = target_pos.left - pos_left.left;


                        left.animate(
                            [
                                {transform: 'translateX(0)'},
                                {transform: 'translateX(' + i + 'px' + ')'},
                            ],
                            {
                                duration:300,
                                easing:'ease',
                                fill:"forwards",
                                iterations:1,
                                delay:0
                            }
                        );

                        i *= -1;

                        right.animate(
                            [
                                {transform: 'translateX(0)'},
                                {transform: 'translateX(' + i + 'px' + ')'},
                            ],
                            {
                                duration:300,
                                easing:'ease',
                                fill:"forwards",
                                iterations:1,
                                delay:0
                            }
                        );

                        var delayInMilliseconds = 600;
                        setTimeout(function() {
                            var c1 = document.createElement('div');
                            c1.classList.add('containers');
                            c1.textContent =containers[0].textContent;
                            c1.style.background = containers[0].style.background;
                            console.log(containers[0].style.background);
                            //c1.style.background = '#DB7093';
                            
                            var c2 = document.createElement('div');
                            c2.classList.add('containers');
                            c2.textContent =containers[1].textContent;
                            c2.style.background = containers[1].style.background;
                            console.log(containers[1].style.background);
                            // c2.style.background = '#3CB371';
                
                            var c3 = document.createElement('div');
                            c3.classList.add('containers');
                            c3.textContent =containers[2].textContent;
                            console.log(containers[2].style.background);
                            c3.style.background = containers[2].style.background;
                            // c3.style.background = '#DDA0DD';

                            
                
                            main.innerHTML = '';
                            main.appendChild(c1);
                            main.appendChild(c3);
                            main.appendChild(c2);


                            setTimeout(function(){
                                document.getElementsByClassName('containers')[1].classList.add('makebigger');
                            },100);

                        }, delayInMilliseconds);
                    },600);

                    setTimeout(function(){
                        freezeClic = false;
                    },2000);
                }
            }
        }

    }

});