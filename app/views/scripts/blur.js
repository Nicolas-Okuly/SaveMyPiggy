let toggle = false;
let oldValue = []
/*
    This function blurs anything that is money when toggled to protect user privacy.
*/
function blurAll() {
    if (!toggle) {
        /* Blur anything sensitive and save the color */
        let moneyItems = document.getElementsByClassName("money");

        for (let i = 0; i < moneyItems.length; i++) {
            oldValue.push(`${getComputedStyle(moneyItems[i]).color}`);
            moneyItems[i].style.filter = "blur(15px)";
            moneyItems[i].style.color = "#000000";
        }

        toggle = true;
        document.getElementById("blurBtn").src = "./icons/eye.svg";
    } else {
        /* Unblur and restore colors */
        let moneyItems = document.getElementsByClassName("money");

        for (let i = 0; i < moneyItems.length; i++) {
            moneyItems[i].style.filter = "blur(0px)";
            moneyItems[i].style.color = oldValue[i];
        }
        oldValue = [];
        toggle = false;
        document.getElementById("blurBtn").src = "./icons/eye-slash.svg";
    }
}