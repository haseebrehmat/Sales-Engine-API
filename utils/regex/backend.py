backend_regex = [
    {
        'tech_stack': 'NodeJS',
        'exp': '(?i)(^|\W)(node([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Ruby on Rails',
        'exp': '(?i)(^|\W)(ror|ruby|ruby[-\s]?on[-\s]?rails|turbo[-\s]?links|side[-\s]?kiq|rails|capybara|hot[-\s]?wire|r[-\s]?spec|mini[-\s]?test)(\W|$)'
    },
    {
        'tech_stack': 'Service Now',
        'exp': '(?i)(^|\W)(service[-\s]now)(\W|$)'
    },
    {
        'tech_stack': 'salesforce',
        'exp': '(?i)(^|\W)(sales[-\s]?force)(\W|$)'
    },
    {
        'tech_stack': 'ios',
        'exp': '(?i)(^|\W)(ios|swift|swift[-\s]?ui|arkit)(\W|$)'
    },
    {
        'tech_stack': 'flutter',
        'exp': '(?i)(^|\W)(flutter|dart)(\W|$)'
    },
    {
        'tech_stack': 'Android',
        'exp': '(?i)(^|\W)(android|kotlin|mobile[-\s]?app|mobile[-\s]?developers?)(\W|$)'
    },
    {
        'tech_stack': 'Ml Engineer',
        'exp': '(?i)(^|\W)(ai|ml|(machine|deep|Scikit)[-\s](learning|learn)|nlp|Keras|PyTorch|image[-\s]processing|Natural Language Processing|Predictive[-\s]Modeler|Computer[-\s]Vision|Open[-\s]?CV|ml[-]?pack|Text[-\s](Mining|Classification)|Artificial[-\s]Intelligence|Voice[-\s]Classification|Re[-\s]?inforcement[-\s]Learning|Artificial|Neural[-\s](Network|Networks))(\W|$)'
    },
    {
        'tech_stack': 'Data Engineering/Data Engineer',
        'exp': '(?i)(^|\W)(data[-\s](engineer(ing)?|Solutions?|Warehouse|Mining|Integration|Center)|big[-\s]?data|ETL[-_\s](developer|Engineer)|integration[-\s](engineer|analyst|architect))(\W|$)'
    },
    {
        'tech_stack': 'Data Science/Data Scientist',
        'exp': '(?i)(^|\W)(data[-\s](science|scientist|Visualization)|pandas|tableau|Matplotlib|Power[-\s]Bi)(\W|$)'
    },
    {
        'tech_stack': 'blockchain',
        'exp': '(?i)(^|\W)(block[-\s]?chain|bit[-\s]?coins?|Byzantine Fault Tolerance|defi|dlt|DApp|Crypto|Crypto[-\s]?currency|Ethereum|solana|solidity|ICOs|Meta[-\s]?verse|Smart[-\s]?(Contracts?)|Solid[-\s]?JS|UTXO|web[-\s]?3|cryptography)(\W|$)'
    },
    {
        'tech_stack': 'Dynamics',
        'exp': '(?i)(^|\W)((ms[-_\s]?)?dynamics(365)?|D[-\s]365)(\W|$)'
    },
    {
        'tech_stack': 'C#/Dot Net',
        'exp': '(?i)(^|\W)(C[-\s]?Sharp|unity|dot[-_\s]?net|c#|asp|net|.net|wpf|net[\s]?core)(\W|$)'
    },
    {
        'tech_stack': 'C/C++',
        'exp': '(?i)(^|\W)(c\+\+|(c|cpp)[-\s](developers?|programmers?|engineers?|programming|programs?|development|code|experts?))(\W|$)'
    },
    {
        'tech_stack': 'PHP',
        'exp': '(?i)(^|\W)(php|lamp|yii|laravel|cakephp|wordpress|magento|codeigniter|lamp[-\s]stack|symphony|alpine[-.\s]?js)(\W|$)'
    },
    {
        'tech_stack': 'Python',
        'exp': '(?i)(^|\W)(python|django|flask|fast[-\s]?api|sql[-\s]?achemy)(\W|$)'
    },
    {
        'tech_stack': 'Go/Golang',
        'exp': '(?i)(^|\W)(go|golang|distributed[-\s]systems?)(\W|$)'
    },
    {
        'tech_stack': 'Java',
        'exp': '(?i)(^|\W)(java|servlets|jpa|spring|spring[-\s]?boot|jpm|core[-\s]java|java8|junit|maven|Eclipse|Scala|Spring MVC|Netbeans|jsp|javaee)(\W|$)'
    },
    {
        'tech_stack': 'React Native',
        'exp': '(?i)(^|\W)(react[-_\s]?native)(\W|$)'
    },
    {
        'tech_stack': 'mern',
        'exp': '(?i)(^|\W)(mern|mean|mven|JavaScript Developers?|React[-.\s]?js|express[-.\s]?js|node[-.\s]?(js)?|Frontend\/React|react)(\W|$)'
    },
    {
        'tech_stack': 'JavaScript',
        'exp': '(?i)(^|\W)(javascript|material[-\s]?ui|mapbox|nest|nest[-.\s]?.js|vue|vue[-.\s]?js|angular|angular[-.\s]?js|nuxt[-.\s]?js|nuxt|npm|yarn|npx|angular|redux|ngrx|ractive[.\s]?js|backbone[.\-\s]?js|proctor|recoil.js|ramda[.\-\s]?js|espresso|gatsbyjs|webdriver.io)(\W|$)'
    },
    {
        'tech_stack': 'Database',
        'exp': '(?i)(^|\W)(database|sql|mysql|oracle(db)?|sqlite|solaris|postgres(sql)?|pl[-\/\s]?sql|ms[-\s]?sql|db|maria[-\s]db|kdb+|dbt|ssrs|ssis|t-sql|redis|relation[-\s]database|nosql|no[-\s]sql|mango[-\s]?(db)?|rdbms|cassandra|arangodb)(\W|$)'
    },
    {
        'tech_stack': 'NodeJS',
        'exp': '(?i)(^|\W)(node([-\s]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Ruby on Rails',
        'exp': '(?i)(^|\W)(ror|ruby|ruby[-\s]?on[-\s]?rails|turbo[-\s]?links|side[-\s]?kiq|rails|capybara|hot[-\s]?wire|r[-\s]?spec|mini[-\s]?test)(\W|$)'
    },
    {
        'tech_stack': 'Service Now',
        'exp': '(?i)(^|\W)(service[-\s]now)(\W|$)'
    },
    {
        'tech_stack': 'salesforce',
        'exp': '(?i)(^|\W)(sales[-\s]?force)(\W|$)'
    },
    {
        'tech_stack': 'ios',
        'exp': '(?i)(^|\W)(ios|swift|cocoa([-\s]?touch)?|swift[-\s]?ui|arkit)(\W|$)'
    },
    {
        'tech_stack': 'flutter',
        'exp': '(?i)(^|\W)(flutter|dart)(\W|$)'
    },
    {
        'tech_stack': 'Android',
        'exp': '(?i)(^|\W)(android|kotlin|mobile[-\s]?app|mobile[-\s]?developers?)(\W|$)'
    },
    {
        'tech_stack': 'Ml Engineer',
        'exp': '(?i)(^|\W)(ai|ml|lightgbm|gnns|core([-\s\_.]?ml)?|(machine|deep|Scikit)[-\s](learning|learn)|nlp|Keras|PyTorch|image[-\s]processing|Natural Language Processing|Predictive[-\s]Modeler|Computer[-\s]Vision|Open[-\s]?CV|ml[-]?pack|Text[-\s](Mining|Classification)|Artificial[-\s]Intelligence|Voice[-\s]Classification|Re[-\s]?inforcement[-\s]Learning|Artificial|Neural[-\s](Network|Networks))(\W|$)'
    },
    {
        'tech_stack': 'Data Engineering/Data Engineer',
        'exp': '(?i)(^|\W)(data[-\s](engineer(ing)?|Solutions?|Warehouse|Mining|Integration|Center)|big[-\s]?data|ETL[-_\s](developer|Engineer)|integration[-\s](engineer|analyst|architect))(\W|$)'
    },
    {
        'tech_stack': 'Data Science/Data Scientist',
        'exp': '(?i)(^|\W)(data[-\s](science|scientist|Visualization)|pandas|tableau|Matplotlib|Power[-\s]Bi)(\W|$)'
    },
    {
        'tech_stack': 'blockchain',
        'exp': '(?i)(^|\W)(block[-\s]?chain|bit[-\s]?coins?|Byzantine Fault Tolerance|defi|dlt|DApp|Crypto|Crypto[-\s]?currency|Ethereum|solana|solidity|ICOs|Meta[-\s]?verse|Smart[-\s]?(Contracts?)|Solid[-\s]?JS|UTXO|web[-\s]?3|cryptography)(\W|$)'
    },
    {
        'tech_stack': 'Dynamics',
        'exp': '(?i)(^|\W)((ms[-_\s]?)?dynamics(365)?|D[-\s]365)(\W|$)'
    },
    {
        'tech_stack': 'C#/Dot Net',
        'exp': '(?i)(^|\W)(C[-\s]?Sharp|unity|dot[-_\s]?net|c#|asp|net|.net|wpf|net[\s]?core)(\W|$)'
    },
    {
        'tech_stack': 'C/C++',
        'exp': '(?i)(^|\W)(c\+\+|(c|cpp)[-\s](developers?|programmers?|engineers?|programming|programs?|development|code|experts?))(\W|$)'
    },
    {
        'tech_stack': 'PHP',
        'exp': '(?i)(^|\W)(php|lamp|yii|laravel|cakephp|wordpress|magento|codeigniter|lamp[-\s]stack|symphony|alpine[-.\s]?js)(\W|$)'
    },
    {
        'tech_stack': 'Python',
        'exp': '(?i)(^|\W)(python|django|flask|pyunit|pyside|drf|eli5|fast[-\s]?api|sql[-\s]?achemy)(\W|$)'
    },
    {
        'tech_stack': 'Go/Golang',
        'exp': '(?i)(^|\W)(go|golang|distributed[-\s]systems?)(\W|$)'
    },
    {
        'tech_stack': 'Java',
        'exp': '(?i)(^|\W)(java|servlets|jms|spring framework|jpa|jee|spring|spring[-\s]?boot|java spring|jpm|core[-\s]java|java8|junit|maven|Eclipse|Scala|Spring MVC|Netbeans|jsp|javaee|spring[-\s]?data)(\W|$)'
    },
    {
        'tech_stack': 'React Native',
        'exp': '(?i)(^|\W)(react[-_\s]?native)(\W|$)'
    },
    {
        'tech_stack': 'mern',
        'exp': '(?i)(^|\W)(mern|mean|mven|JavaScript Developers?|React[-.\s]?js|express[-.\s]?js|node[-.\s]?(js)?|Frontend\/React|react)(\W|$)'
    },
    {
        'tech_stack': 'JavaScript',
        'exp': '(?i)(^|\W)(javascript|material[-\s]?ui|mapbox|nest|nest[-.\s]?.js|vue|vue[-.\s]?js|angular|swc|babel|angular[-.\s]?js|nuxt[-.\s]?js|nuxt|npm|yarn|npx|angular|redux|ngrx|ractive[.\s]?js|backbone[.\-\s]?js|proctor|recoil.js|ramda[.\-\s]?js|espresso|gatsbyjs|webdriver.io)(\W|$)'
    },
    {
        'tech_stack': 'Database',
        'exp': '(?i)(^|\W)(database|sql|mysql|oracle(db)?|sqlite|solaris|postgres(sql)?|pl[-\/\s]?sql|ms[-\s]?sql|db|maria[-\s]db|kdb+|dbt|ssrs|ssis|t-sql|redis|relation[-\s]database|nosql|no[-\s]sql|mango[-\s]?(db)?|rdbms|cassandra|arangodb)(\W|$)'
    },
    {
        'tech_stack': 'Specflow',
        'exp': '(?i)(^|\W)(spec([-\s\_.]?flow)?)(\W|$)'
    },
    {
        'tech_stack': 'Perl',
        'exp': '(?i)(^|\W)(perl)(\W|$)'
    },
    {
        'tech_stack': 'Struts',
        'exp': '(?i)(^|\W)(struts)(\W|$)'
    },
    {
        'tech_stack': 'Shopify',
        'exp': '(?i)(^|\W)(shopify)(\W|$)'
    },
    {
        'tech_stack': 'J2EE',
        'exp': '(?i)(^|\W)(j2ee)(\W|$)'
    },
    {
        'tech_stack': 'Objective C',
        'exp': '(?i)(^|\W)(objective([-\s\_.]?c)?|object([-\s\_.]?c)?)(\W|$)'
    },
    {
        'tech_stack': 'RXJava',
        'exp': '(?i)(^|\W)(rx([-\s\_.]?java)?)(\W|$)'
    },
    {
        'tech_stack': 'UI path',
        'exp': '(?i)(^|\W)(ui([-\s\_.]?path)?)(\W|$)'
    },
    {
        'tech_stack': 'RPA',
        'exp': '(?i)(^|\W)(rpa)(\W|$)'
    },
    {
        'tech_stack': 'Rust',
        'exp': '(?i)(^|\W)(rust)(\W|$)'
    },
    {
        'tech_stack': 'Hascal',
        'exp': '(?i)(^|\W)(hascal)(\W|$)'
    },
    {
        'tech_stack': 'VbScript',
        'exp': '(?i)(^|\W)(vbscript)(\W|$)'
    },
    {
        'tech_stack': 'R Language',
        'exp': '(?i)(^|\W)(r language)(\W|$)'
    },

]



