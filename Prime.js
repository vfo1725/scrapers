const rp = require('request-promise-native');
const fs = require('fs');
const cheerio = require('cheerio');

async function downloadHtmlPrime() {

	const uri = 'https://www.bankrate.com/rates/interest-rates/prime-rate/';
	const filename = 'indexDataPrime.html';

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
		
	console.log('Parsing index rates HTML of Prime...');
	const htmlFilename = 'indexDataPrime.html';
	const html = await fs.promises.readFile(htmlFilename);
	const $ = cheerio.load(html);

    const $trs = $('.table tbody tr');
	const values = {};

    for(let i = 0; i < 4; i++){
      const data = $.html($trs[i]);
      const td = $(data).find('td').toArray();
      const $title = $(td[0]);
      const $tdrates = $(td[1]);
      const key = $title.text();
      const trimmedKey = key.replace(/(\r\n|\n|\r)/gm, "");
      const value = $tdrates.text();
      values[trimmedKey] = isNaN(+value) ? value : +value;
    }

	return values;
}

async function main() {

	console.log('Starting the Scrape...');
	await downloadHtmlPrime();
	const indexes = await parseIndex();

	await fs.promises.writeFile(
		'indexesPrime.json',
		JSON.stringify(indexes, null, 2)
	);
	
	await fs.promises.writeFile(
		'indexesPrime.csv',
		JSON.stringify(indexes, null, 2)
	);

	console.log('Done');
}

main();