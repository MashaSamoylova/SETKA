all:
	mkdir -p _build/ui
	touch _build/ui/__init__.py
	mkdir -p _build/uasyncio
	cp -r ./uasyncio ./_build/
	pyminifier -o ./_build/boot.py boot.py 
	pyminifier -o ./_build/main.py main.py
	pyminifier -o ./_build/ui/screen.py ./ui/screen.py  
	pyminifier -o ./_build/ui/tab1.py ./ui/tab1.py
	pyminifier -o ./_build/ui/tab2.py ./ui/tab2.py
	pyminifier -o ./_build/ui/tab3.py ./ui/tab3.py
	pyminifier -o ./_build/ui/utils.py ./ui/utils.py
	pyminifier -o ./_build/ui/views.py ./ui/views.py
#	pyminifier -o ./_build/uasyncio/core.py ./uasyncio/core.py
	cp -r ./_build/* /media/roman/ARIGATO
	
clean:
	rm -r _build
