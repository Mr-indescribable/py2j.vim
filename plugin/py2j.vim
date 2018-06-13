" Section: setup path of the external python script {{{1
"
" Well, I wrote the path of external script here directly. :(
" Currently, I don't know how to calculte the path of vim plugins in vim
" scripts. And expand(<sfile>) always returns the name of my function,
" it dosn't work as the documentation and other programers said.
" So, I'll keep learning. I'll fix this Once I find out how to calculte
" the path of plugins in a vim script dynamically.
let s:py_generator = "~/.vim/bundle/py2j.vim/plugin/genpojo.py"

" Function: Py2Pojo() {{{1
" This function will replace the selected Python class with Java POJO.
" It invokes an external python script to generate the Java code.
"
" Args:
"   -mode_: The current mode of the editor. This argument is used to verify
"           the mode only. It helps this function to avoid invalid invoking.
"           In other words, the mode_ argument should always be passed into
"           the function like this: Py2Pojo(visualmode())
"
" Returns:
"   nothing
function Py2Pojo(mode_) range
	if a:mode_ != "V"
		echoerr "Function Py2Pojo can only be called in visual-line mode"
		finish
	endif

	let a:lines = getline(a:firstline, a:lastline)
	let a:tempfile = tempname()
	call writefile(a:lines, a:tempfile)

	let a:cmd = "python " . s:py_generator . " " . a:tempfile
	call system(a:cmd)
	let a:pojo_code = readfile(a:tempfile)
	call delete(a:tempfile)

	execute a:firstline . "," . a:lastline . "d"
	call append(a:firstline - 1, a:pojo_code)

endfunction

" Section: map the function {{{1
map <leader>jp :call Py2Pojo(visualmode())<CR>
