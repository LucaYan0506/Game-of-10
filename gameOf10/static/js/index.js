function show_hide_login_view(){
    const rule_view = document.querySelector('#login-container');

    if (rule_view.style.display == 'flex'){
        rule_view.style.display = 'none';
    }else{
        rule_view.style.display = 'flex';
    }
}

function show_hide_register_view(){
    const rule_view = document.querySelector('#register-container');

    if (rule_view.style.display == 'flex'){
        rule_view.style.display = 'none';
    }else{
        rule_view.style.display = 'flex';
    }
}

function confirmation(){
    return confirm("Any previous game will be permanently deleted. Do you wish to continue to create a new game?");
}

document.querySelector('#login-container').addEventListener('click',event => {
    if (event.target == document.querySelector('#login-container')){
        show_hide_login_view()
    }
})