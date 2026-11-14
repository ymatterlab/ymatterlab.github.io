const {chromium}=require('playwright-core');
const AxeBuilder=require('@axe-core/playwright').default;
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const context=await browser.newContext({reducedMotion:'reduce'});
 await context.route('**/*',route=>route.request().url().startsWith('http://127.0.0.1:')?route.continue():route.abort());
 const results=[];
 for(const path of ['/', '/research/','/people/','/publications/','/join/','/news/','/contact/','/disclaimer/']){
  const page=await context.newPage();await page.goto((process.env.AUDIT_BASE||'http://127.0.0.1:8767')+path);
  const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  results.push({path,violations:result.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,html:n.html,summary:n.failureSummary}))})),incomplete:result.incomplete.map(v=>({id:v.id,nodes:v.nodes.length})),passes:result.passes.length});
  console.log(path,JSON.stringify(results.at(-1)));await page.close();
 }
 fs.writeFileSync(process.env.AUDIT_OUTPUT||'/tmp/ymatter-a11y/baseline.json',JSON.stringify(results,null,2));await browser.close();
 if(results.some(r=>r.violations.length)) process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
