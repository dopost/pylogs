<<<<<<< HEAD
function reload_verifycode(oVerifycode) {
    //var oVerifycode = document.getElementById(sVerifycode);
    var now = new Date();
	if (oVerifycode) {
        oVerifycode.src = "/utils/vcode/?date=" + now.getTime(); 
    }
=======
function reload_verifycode(oVerifycode) {
    //var oVerifycode = document.getElementById(sVerifycode);
    var now = new Date();
	if (oVerifycode) {
        oVerifycode.src = "/utils/vcode/?date=" + now.getTime(); 
    }
>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
}