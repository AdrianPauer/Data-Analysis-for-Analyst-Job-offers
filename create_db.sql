CREATE TABLE  jobs (
	id INT,
	title TEXT, 
	salary TEXT,
	description TEXT,
	rating DOUBLE,
	company TEXT,
	location TEXT,
	headquarters TEXT,
	size TEXT,
	founded INT,
	ownership TEXT,
	industry TEXT,
	sector TEXT,
	revenue TEXT,
	competitors TEXT,
	easyApply TEXT
	
);
.mode csv
.import DataAnalyst.csv jobs
