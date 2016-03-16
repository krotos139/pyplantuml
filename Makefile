all: out_statedia.png

out_statedia.txt:
	python project_gen.py

out_statedia.png: out_statedia.txt
	java -jar plantuml.jar out_statedia.txt

clean:
	rm out_plan.csv out_statedia.png out_statedia.txt
view:
	gwenview out_statedia.png
