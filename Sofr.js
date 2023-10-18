const rp = require('request-promise-native');
const fs = require('fs');
const cheerio = require('cheerio');

async function downloadHtmlSOFR() {

	const uri = 'https://markets.newyorkfed.org/read?productCode=50&eventCodes=520&limit=25&startPosition=0&sort=postDt:-1&format=xml';
	const filename = 'indexDataSOFR.html';

	const fileExists = fs.existsSync(filename);
	if (fileExists) {
		console.log('Skipping download since the file ' + filename + ' already exists.');
		return;
	}

	console.log('Downloading HTML from ' + uri);
	const results = await rp({uri: uri});
	await fs.promises.writeFile(filename, results);
}

async function parseIndex() {
		console.log('Parsing index rates HTML of SOFR...');
		const htmlFilename = 'indexDataSOFR.html';
		const html = await fs.promises.readFile(htmlFilename);
		const $ = cheerio.load(html);
		const values = {};
		
		const $trs = $('rate');
		const tr = $trs.toArray();
		const rate = $(tr).find('percentrate').toArray();
		const date = $(tr).find('effectivedate').toArray();
		
		for(let i = 0; i < 5; i++){
			const $rate = $(rate[i]);
			const $date = $(date[i]);
			const value = $rate.text();
			const key = $date.text();
			values[key] = isNaN(+value) ? value : +value;
		}
		
		return values;
}

async function main() {

	console.log('Starting the Scrape...');
	await downloadHtmlSOFR();
	const indexes = await parseIndex();

	await fs.promises.writeFile(
		'indexSOFR.json',
		JSON.stringify(indexes, null, 2)
	);
	
	await fs.promises.writeFile(
		'indexSOFR.csv',
		JSON.stringify(indexes, null, 2)
	);

	console.log('Done');
}

main();
