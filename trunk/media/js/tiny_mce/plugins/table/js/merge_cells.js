<<<<<<< HEAD
tinyMCEPopup.requireLangPack();

function init() {
	var f = document.forms[0], v;

	tinyMCEPopup.resizeToInnerSize();

	f.numcols.value = tinyMCEPopup.getWindowArg('numcols', 1);
	f.numrows.value = tinyMCEPopup.getWindowArg('numcols', 1);
}

function mergeCells() {
	var args = [], f = document.forms[0];

	if (!AutoValidator.validate(f)) {
		alert(tinyMCEPopup.getLang('invalid_data'));
		return false;
	}

	args["numcols"] = f.numcols.value;
	args["numrows"] = f.numrows.value;

	tinyMCEPopup.execCommand("mceTableMergeCells", false, args);
	tinyMCEPopup.close();
}

tinyMCEPopup.onInit.add(init);
=======
tinyMCEPopup.requireLangPack();

function init() {
	var f = document.forms[0], v;

	tinyMCEPopup.resizeToInnerSize();

	f.numcols.value = tinyMCEPopup.getWindowArg('numcols', 1);
	f.numrows.value = tinyMCEPopup.getWindowArg('numcols', 1);
}

function mergeCells() {
	var args = [], f = document.forms[0];

	if (!AutoValidator.validate(f)) {
		alert(tinyMCEPopup.getLang('invalid_data'));
		return false;
	}

	args["numcols"] = f.numcols.value;
	args["numrows"] = f.numrows.value;

	tinyMCEPopup.execCommand("mceTableMergeCells", false, args);
	tinyMCEPopup.close();
}

tinyMCEPopup.onInit.add(init);
>>>>>>> 1b1aba63e4e25c4d81cdc8ee168ba60582ceb029
