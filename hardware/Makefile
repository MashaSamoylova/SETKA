all:
	mkdir -p _build/ui
	touch _build/ui/__init__.py
	mkdir -p _build/uasyncio
	touch _build/uasyncio/__init__.py
	mkdir -p _build/makhina
	mkdir -p _build/recipes
	pyminifier -o ./_build/boot.py boot.py 
	pyminifier -o ./_build/main.py main.py
	pyminifier -o ./_build/ui/screen.py ./ui/screen.py  
	pyminifier -o ./_build/ui/tab1.py ./ui/tab1.py
	pyminifier -o ./_build/ui/tab2.py ./ui/tab2.py
	pyminifier -o ./_build/ui/tab3.py ./ui/tab3.py
	pyminifier -o ./_build/ui/utils.py ./ui/utils.py
	pyminifier -o ./_build/ui/views.py ./ui/views.py
	pyminifier -o ./_build/uasyncio/core.py ./uasyncio/core.py
	pyminifier -o ./_build/makhina/makhina.py ./makhina/makhina.py
	pyminifier -o ./_build/makhina/motor.py ./makhina/motor.py
	pyminifier -o ./_build/makhina/control.py ./makhina/control.py
	
	cp -r ./_build/* /media/${USER}/ARIGATO
	
without_compress:
	mkdir -p _build/ui
	touch _build/ui/__init__.py
	mkdir -p _build/uasyncio
	mkdir -p _build/makhina
	mkdir -p _build/recipes
	touch _build/makhina/__init__.py
	cp boot.py ./_build/boot.py 
	cp main.py ./_build/main.py
	cp ./ui/screen.py ./_build/ui/screen.py  
	cp ./ui/tab1.py ./_build/ui/tab1.py
	cp ./ui/tab2.py ./_build/ui/tab2.py
	cp ./ui/tab3.py ./_build/ui/tab3.py
	cp ./ui/utils.py ./_build/ui/utils.py
	cp ./ui/views.py ./_build/ui/views.py
	cp ./uasyncio/core.py ./_build/uasyncio/core.py
	cp ./uasyncio/__init__.py ./_build/uasyncio/__init__.py
	cp ./makhina/makhina.py ./_build/makhina/makhina.py
	cp ./makhina/motor.py ./_build/makhina/motor.py
	cp ./makhina/control.py ./_build/makhina/control.py
	cp -R ./uModbus ./_build/
	cp mainconfig.py ./_build
	cp pc.py ./_build
	cp -r ./_build/* /media/${USER}/ARIGATO

clean:
	rm -r _build
