core_framework_regex = [
    {
        'tech_stack': 'ReactJS',
        'exp': '(?i)(^|\W)(react([-_.\s]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'AngularJS',
        'exp': '(?i)(^|\W)(angular([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'VueJS',
        'exp': '(?i)(^|\W)(vue([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'MustacheJS',
        'exp': '(?i)(^|\W)(mustache([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'HandlebarsJS',
        'exp': '(?i)(^|\W)(handlebars([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Webforms',
        'exp': '(?i)(^|\W)(web([-_\s]?forms)?)(\W|$)'
    },
    {
        'tech_stack': 'SvelteJS',
        'exp': '(?i)(^|\W)(svelte([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Webpack',
        'exp': '(?i)(^|\W)(web([-_\s]?pack)?)(\W|$)'
    },
    {
        'tech_stack': 'ImmutableJS',
        'exp': '(?i)(^|\W)(Immutable([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'PanniJS',
        'exp': '(?i)(^|\W)(panni([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'DustJS',
        'exp': '(?i)(^|\W)(dust([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Redux',
        'exp': '(?i)(^|\W)(redux)(\W|$)'
    },
    {
        'tech_stack': 'PHP',
        'exp': '(?i)(^|\W)(php)(\W|$)'
    },
    {
        'tech_stack': 'Laravel',
        'exp': '(?i)(^|\W)(laravel)(\W|$)'
    },
    {
        'tech_stack': 'Phalcon',
        'exp': '(?i)(^|\W)(phalcon)(\W|$)'
    },
    {
        'tech_stack': 'Yii',
        'exp': '(?i)(^|\W)(yii)(\W|$)'
    },
    {
        'tech_stack': 'CodeIgniter',
        'exp': '(?i)(^|\W)(code([-\s\_.]?igniter)?)(\W|$)'
    },
    {
        'tech_stack': 'Symfony',
        'exp': '(?i)(^|\W)(symfony)(\W|$)'
    },
    {
        'tech_stack': 'Composer',
        'exp': '(?i)(^|\W)(composer)(\W|$)'
    },
    {
        'tech_stack': 'Joomla',
        'exp': '(?i)(^|\W)(joomla)(\W|$)'
    },
    {
        'tech_stack': 'Smarty',
        'exp': '(?i)(^|\W)(smarty)(\W|$)'
    },
    {
        'tech_stack': 'Magento',
        'exp': '(?i)(^|\W)(magento)(\W|$)'
    },
    {
        'tech_stack': 'WordPress',
        'exp': '(?i)(^|\W)(word([-\s\_.]?press)?)(\W|$)'
    },
    {
        'tech_stack': 'C#',
        'exp': '(?i)(^|\W)(c([-\s\_.]?#)?)(\W|$)'
    },
    {
        'tech_stack': '.Net',
        'exp': '(?i)(^|\W)(.([-\s\_.]?net)?)(\W|$)'
    },
    {
        'tech_stack': ' DotNet',
        'exp': '(?i)(^|\W)(dot([-\s\_.]?net)?)(\W|$)'
    },
    {
        'tech_stack': ' Dot Net Core',
        'exp': '(?i)(^|\W)(dot([-\s\_.]?net([-\s\_.]?core)?)?)(\W|$)'
    },
    {
        'tech_stack': ' .Net Core',
        'exp': '(?i)(^|\W)(.([-\s\_.]?net([-\s\_.]?core)?)?)(\W|$)'
    },
    {
        'tech_stack': 'ASP .net',
        'exp': '(?i)(^|\W)(asp([-\s\_.]?.([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'ASP DotNet',
        'exp': '(?i)(^|\W)(asp([-\s\_.]?dot([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'Entity',
        'exp': '(?i)(^|\W)(entity)(\W|$)'
    },
    {
        'tech_stack': 'ADO .net',
        'exp': '(?i)(^|\W)(ado([-\s\_.]?.([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'ADO DotNet',
        'exp': '(?i)(^|\W)(ado([-\s\_.]?dot([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'VB .net',
        'exp': '(?i)(^|\W)(vb([-\s\_.]?.([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'VB DotNet',
        'exp': '(?i)(^|\W)(vb([-\s\_.]?dot([-\s\_.]?net)?)?)(\W|$)'
    },
    {
        'tech_stack': 'Java',
        'exp': '(?i)(^|\W)(java)(\W|$)'
    },
    {
        'tech_stack': 'Spring Boot',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?boot)?)(\W|$)'
    },
    {
        'tech_stack': 'J2EE',
        'exp': '(?i)(^|\W)(j2ee)(\W|$)'
    },
    {
        'tech_stack': 'JPA',
        'exp': '(?i)(^|\W)(jpa)(\W|$)'
    },
    {
        'tech_stack': 'Python',
        'exp': '(?i)(^|\W)(python)(\W|$)'
    },
    {
        'tech_stack': 'Micronaut',
        'exp': '(?i)(^|\W)(micro([-\s\_.]?naut)?)(\W|$)'
    },
    {
        'tech_stack': 'Kotlin',
        'exp': '(?i)(^|\W)(kotlin)(\W|$)'
    },
    {
        'tech_stack': 'Struts iBATIS',
        'exp': '(?i)(^|\W)(struts([-\s\_.]?ibatis)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring MVC',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?mvc)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring Core',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?core)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring AOP',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?aop)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring Data',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?data)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring Security',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?security)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring Actuator',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?actuator)?)(\W|$)'
    },
    {
        'tech_stack': 'Core Python',
        'exp': '(?i)(^|\W)(core([-\s\_.]?python)?)(\W|$)'
    },
    {
        'tech_stack': 'Django',
        'exp': '(?i)(^|\W)(django)(\W|$)'
    },
    {
        'tech_stack': 'Flask',
        'exp': '(?i)(^|\W)(flask)(\W|$)'
    },
    {
        'tech_stack': 'Marionette',
        'exp': '(?i)(^|\W)(marionette)(\W|$)'
    },
    {
        'tech_stack': 'Java Spring',
        'exp': '(?i)(^|\W)(java([-\s\_.]?spring)?)(\W|$)'
    },
    {
        'tech_stack': 'Boot Spring',
        'exp': '(?i)(^|\W)(boot([-\s\_.]?spring)?)(\W|$)'
    },
    {
        'tech_stack': 'Typescript',
        'exp': '(?i)(^|\W)(type([-\s\_.]?script)?)(\W|$)'
    },
    {
        'tech_stack': 'HapiJS',
        'exp': '(?i)(^|\W)(hapi([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'FastiFyJS',
        'exp': '(?i)(^|\W)(fastify([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'NestJS',
        'exp': '(?i)(^|\W)(nest([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'MeteorJS',
        'exp': '(?i)(^|\W)(meteor([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Javascript',
        'exp': '(?i)(^|\W)(javascript)(\W|$)'
    },
    {
        'tech_stack': 'ES6',
        'exp': '(?i)(^|\W)(es6)(\W|$)'
    },
    {
        'tech_stack': 'NextJS',
        'exp': '(?i)(^|\W)(next([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'ECMAScript6',
        'exp': '(?i)(^|\W)(ecma([-\s\_.]?script([-\s\_.]?6)?)?)(\W|$)'
    },
    {
        'tech_stack': 'ExpressJS',
        'exp': '(?i)(^|\W)(express([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'ExtJS',
        'exp': '(?i)(^|\W)(ext([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'React Native',
        'exp': '(?i)(^|\W)(react([-\s\_.]?native)?)(\W|$)'
    },
    {
        'tech_stack': 'BackboneJS',
        'exp': '(?i)(^|\W)(backbone([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'jQuery',
        'exp': '(?i)(^|\W)(j([-\s\_.]?query)?)(\W|$)'
    },
    {
        'tech_stack': 'NuxtJS',
        'exp': '(?i)(^|\W)(nuxt([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Pyramid',
        'exp': '(?i)(^|\W)(pyramid)(\W|$)'
    },
    {
        'tech_stack': 'NumPy',
        'exp': '(?i)(^|\W)(num([-\s\_.]?py)?)(\W|$)'
    },
    {
        'tech_stack': 'PyTest',
        'exp': '(?i)(^|\W)(py([-\s\_.]?test)?)(\W|$)'
    },
    {
        'tech_stack': 'PyUnit',
        'exp': '(?i)(^|\W)(py([-\s\_.]?unit)?)(\W|$)'
    },
    {
        'tech_stack': 'Falcon',
        'exp': '(?i)(^|\W)(falcon)(\W|$)'
    },
    {
        'tech_stack': 'Giotto',
        'exp': '(?i)(^|\W)(giotto)(\W|$)'
    },
    {
        'tech_stack': 'Growler',
        'exp': '(?i)(^|\W)(growler)(\W|$)'
    },
    {
        'tech_stack': 'Pylons',
        'exp': '(?i)(^|\W)(pylons)(\W|$)'
    },
    {
        'tech_stack': 'Python Scripting',
        'exp': '(?i)(^|\W)(python([-\s\_.]?scripting)?)(\W|$)'
    },
    {
        'tech_stack': 'AI',
        'exp': '(?i)(^|\W)(ai)(\W|$)'
    },
    {
        'tech_stack': 'Salt',
        'exp': '(?i)(^|\W)(salt)(\W|$)'
    },
    {
        'tech_stack': 'NLP',
        'exp': '(?i)(^|\W)(nlp)(\W|$)'
    },
    {
        'tech_stack': 'Native',
        'exp': '(?i)(^|\W)(native)(\W|$)'
    },
    {
        'tech_stack': 'Android',
        'exp': '(?i)(^|\W)(android)(\W|$)'
    },
    {
        'tech_stack': 'Microservices',
        'exp': '(?i)(^|\W)(micro([-\s\_.]?services)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring JPA',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?jpa)?)(\W|$)'
    },
    {
        'tech_stack': 'Ebean',
        'exp': '(?i)(^|\W)(e([-\s\_.]?bean)?)(\W|$)'
    },
    {
        'tech_stack': 'Spring Transactions',
        'exp': '(?i)(^|\W)(spring([-\s\_.]?transactions)?)(\W|$)'
    },
    {
        'tech_stack': 'Design Patterns',
        'exp': '(?i)(^|\W)(Design([-\s\_.]?Patterns)?)(\W|$)'
    },
    {
        'tech_stack': 'Junit',
        'exp': '(?i)(^|\W)(junit)(\W|$)'
    },
    {
        'tech_stack': 'Cypress',
        'exp': '(?i)(^|\W)(cypress)(\W|$)'
    },
    {
        'tech_stack': 'Mockito',
        'exp': '(?i)(^|\W)(mockito)(\W|$)'
    },
    {
        'tech_stack': 'Appium 11',
        'exp': '(?i)(^|\W)(Appium([-\s\_.]?11)?)(\W|$)'
    },
    {
        'tech_stack': 'TestNG 11',
        'exp': '(?i)(^|\W)(testng([-\s\_.]?11)?)(\W|$)'
    },
    {
        'tech_stack': 'Jest',
        'exp': '(?i)(^|\W)(jest)(\W|$)'
    },
    {
        'tech_stack': 'Craft Automation',
        'exp': '(?i)(^|\W)(craft([-\s\_.]?automation)?)(\W|$)'
    },
    {
        'tech_stack': 'JBehave',
        'exp': '(?i)(^|\W)(j([-\s\_.]?behave)?)(\W|$)'
    },
    {
        'tech_stack': 'XCUI',
        'exp': '(?i)(^|\W)(xcui)(\W|$)'
    },
    {
        'tech_stack': 'NUnit',
        'exp': '(?i)(^|\W)(n([-\s\_.]?unit)?)(\W|$)'
    },
    {
        'tech_stack': 'Nightwatch JS',
        'exp': '(?i)(^|\W)(night([-\s\_.]?watch([-\s\_.]?js)?)?)(\W|$)'
    },
    {
        'tech_stack': 'K6',
        'exp': '(?i)(^|\W)(k6)(\W|$)'
    },
    {
        'tech_stack': 'Selenium Webdriver',
        'exp': '(?i)(^|\W)(selenium([-\s\_.]?webdriver)?)(\W|$)'
    },
    {
        'tech_stack': 'UFT',
        'exp': '(?i)(^|\W)(uft)(\W|$)'
    },
    {
        'tech_stack': 'Soap UI',
        'exp': '(?i)(^|\W)(soap([-\s\_.]?ui)?)(\W|$)'
    },
    {
        'tech_stack': 'Cucumber',
        'exp': '(?i)(^|\W)(cucumber)(\W|$)'
    },
    {
        'tech_stack': 'Maven',
        'exp': '(?i)(^|\W)(maven)(\W|$)'
    },
    {
        'tech_stack': 'JMeter',
        'exp': '(?i)(^|\W)(j([-\s\_.]?meter)?)(\W|$)'
    },
    {
        'tech_stack': 'Selenium Grid',
        'exp': '(?i)(^|\W)(selenium([-\s\_.]?grid)?)(\W|$)'
    },
    {
        'tech_stack': 'Shift Left',
        'exp': '(?i)(^|\W)(shift([-\s\_.]?left)?)(\W|$)'
    },
    {
        'tech_stack': 'Katalon',
        'exp': '(?i)(^|\W)(katalon)(\W|$)'
    },
    {
        'tech_stack': 'Calabash',
        'exp': '(?i)(^|\W)(calabash)(\W|$)'
    },
    {
        'tech_stack': 'Espresso',
        'exp': '(?i)(^|\W)(espresso)(\W|$)'
    },
    {
        'tech_stack': 'Swift UI',
        'exp': '(?i)(^|\W)(swift([-\s\_.]?ui)?)(\W|$)'
    },
    {
        'tech_stack': 'Objective C',
        'exp': '(?i)(^|\W)(objective([-\s\_.]?c)?)(\W|$)'
    },
    {
        'tech_stack': 'Core Graphics',
        'exp': '(?i)(^|\W)(core([-\s\_.]?graphics)?)(\W|$)'
    },
    {
        'tech_stack': 'RxCocoa',
        'exp': '(?i)(^|\W)(rx([-\s\_.]?cocoa)?)(\W|$)'
    },
    {
        'tech_stack': 'RxSwift',
        'exp': '(?i)(^|\W)(rx([-\s\_.]?swift)?)(\W|$)'
    },
    {
        'tech_stack': 'Combine',
        'exp': '(?i)(^|\W)(combine)(\W|$)'
    },
    {
        'tech_stack': 'Interface Builder',
        'exp': '(?i)(^|\W)(interface([-\s\_.]?builder)?)(\W|$)'
    },
    {
        'tech_stack': 'Auto Layout',
        'exp': '(?i)(^|\W)(auto([-\s\_.]?layout)?)(\W|$)'
    },
    {
        'tech_stack': 'Delegates',
        'exp': '(?i)(^|\W)(delegates)(\W|$)'
    },
    {
        'tech_stack': 'Core Data',
        'exp': '(?i)(^|\W)(core([-\s\_.]?data)?)(\W|$)'
    },
    {
        'tech_stack': 'Clean Architecture',
        'exp': '(?i)(^|\W)(clean([-\s\_.]?architecture)?)(\W|$)'
    },
    {
        'tech_stack': 'SOLID Principles',
        'exp': '(?i)(^|\W)(solid([-\s\_.]?principles)?)(\W|$)'
    },
    {
        'tech_stack': 'CoreML',
        'exp': '(?i)(^|\W)(core([-\s\_.]?ml)?)(\W|$)'
    },
    {
        'tech_stack': 'XCode',
        'exp': '(?i)(^|\W)(x([-\s\_.]?code)?)(\W|$)'
    },
    {
        'tech_stack': 'iOS SDKs',
        'exp': '(?i)(^|\W)(ios([-\s\_.]?sdks)?)(\W|$)'
    },
    {
        'tech_stack': 'Storyboard',
        'exp': '(?i)(^|\W)(story([-\s\_.]?board)?)(\W|$)'
    },
    {
        'tech_stack': 'Swinject',
        'exp': '(?i)(^|\W)(swin([-\s\_.]?ject)?)(\W|$)'
    },
    {
        'tech_stack': 'Flutter',
        'exp': '(?i)(^|\W)(flutter)(\W|$)'
    },
    {
        'tech_stack': 'Widgets',
        'exp': '(?i)(^|\W)(widgets)(\W|$)'
    },
    {
        'tech_stack': 'Dart',
        'exp': '(?i)(^|\W)(dart)(\W|$)'
    },
    {
        'tech_stack': 'Node JS',
        'exp': '(?i)(^|\W)(node([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Stencil JS',
        'exp': '(?i)(^|\W)(stencil([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'Stencil JS',
        'exp': '(?i)(^|\W)(stencil([-\s\_.]?js)?)(\W|$)'
    },
    {
        'tech_stack': 'PrimeNG',
        'exp': '(?i)(^|\W)(prime([-\s\_.]?ng)?)(\W|$)'
    },
]



import re

tech = [
    'wordpress',
    'php',
    'cms',
    'ecommerce',
    'corephp',
    'websitebuilder',
    'webprogramming',
    'webdevelopment',
    'websitearhitecure',
    'themecustomization',
    'plugincustomization',
    'blade',
    'plugincreation',
    'gutenberg',
    'querymonitor',
    'buddypress',
    'ror',
    'rails',
    'ruby'
    'liquidslim',
    'laravel', 'cakephp', 'codeigniter', 'wordpress', 'yii', 'symfony', 'php', 'li3', 'fuelphp', 'slim', 'phpixie',
    'fatfree', 'drupal', 'kohana', 'phalcon', 'nette', 'magento', 'joomla',
    'ci/cd', 'kubernetes', 'docker', 'jenkins', 'terraform', 'aws', 'ansible', 'chef', 'rds', 'salt', 'powershell', 'cloudformation', 'arm', 'templates', 'azuredevops', 'eks', 'podman', 'shell', 'scripting', 'aws', 'cloudformation', 'pivotal', 'cloudfoundry', 'aks', 'gke', 'aws', 'cloudwatch', 'gce', 'load', 'balancer', 'microservices', 'microsoft', 'gpo', 'iam', 'tekton', 'iaac', 'azcli', 'quicksight', 'docker', 'hub',
    'bert', 'dialogflow', 'machinelearning', 'deeplearning', 'conversationalai', 'python','c/c++', 'c++', 'cuda', 'pytorch', 'tenserflow', 'opencv', 'golang', 'ruby', 'cnn', 'lstm', 'rnn', 'computervision', 'detectron', 'basicr', 'nlp', 'nlu', 'fluxjl', 'bashscript', 'snowflake', 'hive', 'caffe', 'ml/ai', 'dod', 'torch',
    'solidity', 'nft', 'web3js', 'solana', 'golang', 'ethersjs', 'threejs', 'rust', 'haskell', 'cryptography', 'scala', 'ethereum', 'ganache', 'maticblockchain', 'walletconnect', 'polygon', 'testnets',
    'java', 'springboot', 'j2ee/jee', 'spring', 'microservices', 'springmvc', 'mvcstruts', 'ibatis', 'cucumber', 'soaflink', 'mybatis', 'log4j', 'esb', 'springdata', 'springjpa', 'ebean', 'javascript', 'typescript', 'expressjs', 'j2ee', 'designpatterns', 'mvvm', 'dropwizard', 'stenciljs', 'php', 'laravel', 'wordpress', 'yiisymfony', 'zend', 'codeigniter', 'zikula', 'li3', 'cakephp', 'fuelphp', 'phpixie', 'fatfree', 'drupal', 'kohana', 'phalcon', 'nette', 'python', 'django', 'pyramid', 'drf', 'graphql', 'solidity', 'nft', 'web3solana', 'flaskgolang', 'ethersjs', 'nextjs', 'threejs', 'rusthaskell', 'swift', 'objectivec', 'swiftui', 'coregraphics', 'rxcocoa', 'mvc/mvvm', 'reactnative', 'restfastapi', 'statemanagement', 'android', 'ios', 'nodejs', 'objectivec', 'c#', 'aspnet', 'ror', 'expressnest', 'liquid', 'slim', 'designspatterns', 'rest/soap', 'flutter', 'kotlin', 'dart', 'designswift', 'cms', 'ecommerce', 'corephp', 'websitebuilder', 'websitearhitecure', 'themecustomization', 'plugincustomization', 'bertmachinelearning', 'deeplearning', 'conversationalai', 'go', 'c++', 'cuda', 'pytorch', 'tenserflow', 'opencv', 'guicore', 'erlang', 'cnn', 'lstm', 'rnn', 'computervision', 'detectron', 'basicr', 'dialogflow', 'nlp', 'nlu', 'fluxjl', 'bashscript', 'snowflake', 'hapijs', 'fastifyjs', 'meteorjs', 'marionette', 'serverless', 'ruby', 'starlite', 'koa', 'entity', 'adonet', 'vbnet', 'springcore', 'springaop', 'springsecurity', 'springdata', 'unity', 'linq', 'aurelia', 'objectiveswiftui',
    'kotlin', 'java', 'flutter', 'designpatterns', 'mvc/mvvm', 'nativeandroid', 'springboot', 'swift', 'objectivec', 'swiftui', 'coregraphics', 'rxcocoa', 'ios', 'android', 'dart', 'statemanagement',
    'itom', 'itsm', 'itam', 'itomsuites', 'itsm/itsmpro', 'itommodules', 'pmp', 'servicecatalog', 'tableau', 'grc', 'csa', 'hris', 'cad', 'cis', 'ui/forms', 'c2c', 'rpi', 'ssas', 'ssis', 'ssrs', 'vbnet', 'hcltech', 'updatesets', 'servicemapping', 'wsdl', 'acls', 'siem', 'appengine', 'emr', 'informatica', 'hrsd', 'onboardingandtransitionsmodules', 'itil', 'sam', 'ham', 'iwms', 'nuvolo'
]
