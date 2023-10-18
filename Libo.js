const rp = require('request-promise-native');
const fs = require('fs');
const cheerio = require('cheerio');

async function downloadHtml() {

	const uri = 'https://www.global-rates.com/en/interest-rates/libor/american-dollar/usd-libor-interest-rate-1-month.aspx';
	const filename = 'indexDataGlobal.html';

	const fileExists = fs.existsSync(filename);
	if (fileExists) {
		console.log('Skipping download since the file ' + filename + ' already exists.');
		return;
	}

	console.log('Downloading HTML from ' + uri);
	const results = await rp({uri: uri});
	await fs.promises.writeFile(filename, results);
}

async function parseIndex(){

	console.log('Parsing index Rates HTML of LIBO...');
	const htmlFilename = 'indexDataGlobal.html';
	const html = await fs.promises.readFile(htmlFilename);
	const $ = cheerio.load(html);
	const $trs = $('.maintable tbody tr.tabledata1, .maintable tbody tr.tabledata2');

	const values = {};

	for(let i = 0; i < 5; i++){
		const data = $.html($trs[i]);
		const td = $(data).find('td').toArray();
		const $tdates = $(td[0]);
		const $tdrates = $(td[1]);
		const key = $tdates.text();
		const value = $tdrates.text();

		values[key] = isNaN(+value) ? value : +value;
	}

	return values;
}

async function main(){

	console.log('Starting the Scrape...');
	await downloadHtml();
	const indexes = await parseIndex();

	await fs.promises.writeFile(
		'indexLibo.json',
		JSON.stringify(indexes, null, 2)
	);

	await fs.promises.writeFile(
		'indexLibo.csv',
		JSON.stringify(indexes, null, 2)
	);

	console.log('Done');
}

main();
