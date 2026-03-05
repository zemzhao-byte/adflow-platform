from fastapi import APIRouter
from app.common.schemas import APIResponse

router = APIRouter(prefix="/api/architecture", tags=["产品架构"])

PIPELINE = {
    "title": "海外投放全链路",
    "desc": "从投放准备到数据复盘的完整闭环，每个阶段对应平台的核心能力模块",
    "stages": [
        {"id": "prepare", "name": "投放准备", "color": "#4e83fd",
         "desc": "开户·归因SDK·事件埋点·素材准备",
         "items": ["平台开户(BM/BC)", "MMP SDK接入", "事件埋点配置", "追踪链接生成", "素材规格制作"]},
        {"id": "create", "name": "广告创编", "color": "#36cfc9",
         "desc": "Campaign三层结构搭建·全流程配置",
         "items": ["选择投放目标", "Campaign配置", "Ad Set定向与出价", "Ad素材绑定", "Dry-run校验"]},
        {"id": "launch", "name": "投放上线", "color": "#ffc53d",
         "desc": "提交审核→Learning Phase→逐步放量",
         "items": ["平台审核", "Learning Phase", "预算爬坡", "多平台同步上线"]},
        {"id": "optimize", "name": "投放优化", "color": "#73d13d",
         "desc": "基于实时数据持续调优预算·出价·素材·定向",
         "items": ["实时监控", "预算调控", "出价调优", "素材轮替", "定向拓展"]},
        {"id": "automate", "name": "自动化规则", "color": "#b37feb",
         "desc": "规则引擎7×24自动止损·加量·告警",
         "items": ["止损规则", "加量规则", "素材替换", "异常告警", "定时调度"]},
        {"id": "analyze", "name": "数据分析", "color": "#ff7a45",
         "desc": "多维报表·归因分析·LTV预测·策略复盘",
         "items": ["实时报表", "归因分析", "Cohort/LTV", "跨渠道对比", "策略复盘"]},
    ],
}

ARCH_DIAGRAM = {
    "title": "系统架构全景",
    "desc": "自动化投放平台完整分层架构，覆盖从账户接入到数据复盘的全链路。点击任意模块可展开查看功能点清单。",
    "layers": [
        {"name": "账户与资产管理", "color": "#389e0d", "desc": "投放的基础：账户接入、资产配置、财务管理", "modules": [
            {"name": "平台账户管理", "icon": "Ac", "status": "done", "features": [
                {"f": "多渠道账户绑定(Meta BM/Google MCC/TikTok BC/AppLovin)", "p": "P0"},
                {"f": "Token 安全存储与自动刷新(AES-256加密)", "p": "P0"},
                {"f": "账户状态监控(ACTIVE/DISABLED/PENDING_REVIEW)", "p": "P0"},
                {"f": "账户增删改查 + 批量导入", "p": "P0"},
                {"f": "账户-应用-代理 三级关联关系维护", "p": "P1"},
                {"f": "账户余额/花费上限预警", "p": "P2"},
            ]},
            {"name": "应用管理", "icon": "Ap", "status": "todo", "features": [
                {"f": "App 注册(Package Name/Bundle ID + 商店链接)", "p": "P0"},
                {"f": "MMP SDK 状态检测(已集成/未集成/版本过期)", "p": "P0"},
                {"f": "事件埋点清单管理(af_purchase/af_level等)", "p": "P1"},
                {"f": "OneLink/追踪链接 模板管理", "p": "P1"},
                {"f": "App 与账户的绑定关系维护", "p": "P0"},
            ]},
            {"name": "渠道返点管理", "icon": "$", "status": "done", "features": [
                {"f": "代理商信息维护(名称/联系方式/关联渠道)", "p": "P0"},
                {"f": "固定返点率配置(按时间段+代理+渠道)", "p": "P0"},
                {"f": "阶梯返点配置(消耗区间 → 对应返点率)", "p": "P0"},
                {"f": "扣款/结算记录管理(服务费/罚款/返点发放)", "p": "P0"},
                {"f": "返点自动计算与对账报表", "p": "P2"},
            ]},
        ]},
        {"name": "广告投放层", "color": "#36cfc9", "desc": "优化师日常核心操作：从创编到素材到模板的完整投放工作流", "modules": [
            {"name": "广告创编", "icon": "Ca", "status": "done", "features": [
                {"f": "6步创编向导(平台→目标→Campaign→AdSet→Ad→预览)", "p": "P0"},
                {"f": "渠道特定配置项自动适配(Meta Advantage+/Google UAC)", "p": "P0"},
                {"f": "每步严格校验+阻断(必填项/格式/业务规则)", "p": "P0"},
                {"f": "Dry-run 预校验(validation_only=true)", "p": "P0"},
                {"f": "批量创编(多地区/多素材 自动交叉组合)", "p": "P1"},
                {"f": "跨平台同步上线(同一素材推送多渠道)", "p": "P1"},
                {"f": "Campaign 命名规则引擎({App}_{Geo}_{Obj}_{Date})", "p": "P1"},
            ]},
            {"name": "素材管理", "icon": "Cr", "status": "partial", "features": [
                {"f": "素材上传+格式校验(分辨率/时长/大小/编码)", "p": "P0"},
                {"f": "素材标签分类(类型/语言/地区/风格/AB版本)", "p": "P0"},
                {"f": "智能裁剪(16:9/9:16/1:1 三比例自动生成)", "p": "P1"},
                {"f": "素材效果看板(CTR/CVR/CPI/IPM 趋势)", "p": "P1"},
                {"f": "疲劳度监控(CTR连续下降 → 自动推荐替换)", "p": "P2"},
                {"f": "素材与平台规格自动适配(Meta≤240s/TikTok≤60s等)", "p": "P0"},
            ]},
            {"name": "广告模板", "icon": "Te", "status": "done", "features": [
                {"f": "全流程模板保存与加载(完整创编配置一键复用)", "p": "P0"},
                {"f": "定向模板(T1-iOS-Core/SEA-Android-Broad等)", "p": "P1"},
                {"f": "素材组模板(素材+文案+CTA 组合)", "p": "P1"},
                {"f": "模板搜索/分类/编辑/删除", "p": "P0"},
                {"f": "模板使用频次统计与推荐", "p": "P2"},
            ]},
            {"name": "广告运营", "icon": "Op", "status": "todo", "features": [
                {"f": "Campaign 列表管理(筛选/排序/状态切换)", "p": "P0"},
                {"f": "批量启停/调预算/调出价", "p": "P0"},
                {"f": "预算爬坡策略(每日+20%上限保护)", "p": "P1"},
                {"f": "素材轮替管理(到期自动替换)", "p": "P2"},
                {"f": "A/B Test 管理(对照组/实验组/统计显著性)", "p": "P2"},
            ]},
        ]},
        {"name": "平台对接层", "color": "#4e83fd", "desc": "统一对接各广告平台API，屏蔽平台差异，提供标准化接口", "modules": [
            {"name": "统一Connector", "icon": "Co", "status": "partial", "features": [
                {"f": "BaseConnector 抽象接口(认证/账户/Campaign/AdSet/Ad/报表)", "p": "P0"},
                {"f": "Meta Connector(Graph API v21.0+, Advantage+)", "p": "P0"},
                {"f": "Google Connector(Ads API v18, UAC/PMax)", "p": "P0"},
                {"f": "TikTok Connector(Business API v1.3)", "p": "P1"},
                {"f": "AppLovin Connector(Management API v1)", "p": "P2"},
                {"f": "统一错误码映射(平台错误 → 内部错误码)", "p": "P0"},
            ]},
            {"name": "字段映射引擎", "icon": "Mp", "status": "todo", "features": [
                {"f": "统一数据模型 → 各平台API字段双向映射", "p": "P0"},
                {"f": "目标映射(APP_INSTALL → Meta OUTCOME_APP_PROMOTION / Google MULTI_CHANNEL)", "p": "P0"},
                {"f": "出价策略映射(BID_CAP → 各平台对应字段)", "p": "P0"},
                {"f": "版位映射(统一版位名 → 平台placement ID)", "p": "P1"},
                {"f": "映射规则可配置化(管理后台维护)", "p": "P2"},
            ]},
            {"name": "API弹性机制", "icon": "Re", "status": "todo", "features": [
                {"f": "限流处理(读取x-business-use-case-usage头/X-RateLimit头)", "p": "P0"},
                {"f": "指数退避重试(tenacity, 最多3次)", "p": "P0"},
                {"f": "幂等保障(写操作携带idempotency_key)", "p": "P0"},
                {"f": "熔断器(连续失败超阈值 → 暂停该平台调用)", "p": "P1"},
                {"f": "请求队列与并发控制(Token Bucket算法)", "p": "P1"},
            ]},
        ]},
        {"name": "数据与归因层", "color": "#ff7a45", "desc": "对接MMP归因平台，拉取平台报表，融合计算核心投放指标", "modules": [
            {"name": "归因数据接入", "icon": "AF", "status": "todo", "features": [
                {"f": "AppsFlyer Pull API 对接(Install/Event/Revenue)", "p": "P0"},
                {"f": "AppsFlyer Push API(实时Callback接收Postback)", "p": "P0"},
                {"f": "Adjust Callback + Pull API 对接", "p": "P1"},
                {"f": "SKAN 4.0 数据解析(Coarse/Fine Conversion Value映射)", "p": "P1"},
                {"f": "Google Privacy Sandbox 适配", "p": "P2"},
            ]},
            {"name": "数据报表", "icon": "Da", "status": "partial", "features": [
                {"f": "实时数据仪表盘(Spend/Install/CPI/ROAS 核心KPI)", "p": "P0"},
                {"f": "多维报表(时间/平台/地区/Campaign/素材/设备)", "p": "P0"},
                {"f": "数据融合(MMP归因为准 + 平台Spend → 衍生指标)", "p": "P0"},
                {"f": "Cohort/LTV 分析(D1-D365留存+付费+ROAS)", "p": "P1"},
                {"f": "跨渠道对比报表(同维度对比不同渠道效果)", "p": "P1"},
                {"f": "数据回溯机制(归因窗口内数据持续修正)", "p": "P1"},
                {"f": "报表导出(CSV/Excel/API)", "p": "P0"},
            ]},
            {"name": "数据仓库", "icon": "DW", "status": "todo", "features": [
                {"f": "PostgreSQL 存储业务数据(账户/Campaign/规则)", "p": "P0"},
                {"f": "ClickHouse 存储时序分析数据(报表/指标)", "p": "P1"},
                {"f": "ETL 管道(平台数据 → 清洗 → 入库)", "p": "P0"},
                {"f": "物化视图(预聚合高频查询指标)", "p": "P1"},
                {"f": "数据保留策略(热/温/冷分层)", "p": "P2"},
            ]},
        ]},
        {"name": "智能化层", "color": "#b37feb", "desc": "规则引擎自动化盯盘、预算分配、异常检测，替代人工7×24操盘", "modules": [
            {"name": "规则引擎", "icon": "Ru", "status": "partial", "features": [
                {"f": "条件+动作规则配置(AND/OR + >/</>=/≤/=/!=)", "p": "P0"},
                {"f": "止损规则(CPI>目标×1.3且消耗>$50 → 暂停)", "p": "P0"},
                {"f": "加量规则(CPI<目标×0.8且运行>2天 → 预算+20%)", "p": "P0"},
                {"f": "零转化止损(消耗>$30且Install=0 → 暂停)", "p": "P0"},
                {"f": "素材疲劳规则(CTR连续3天下降 → 暂停素材)", "p": "P1"},
                {"f": "冷却期(调整后N小时不再触发同类规则)", "p": "P0"},
                {"f": "执行模式(自动执行/人工审批)", "p": "P0"},
                {"f": "执行日志审计(时间/对象/条件值/动作/结果)", "p": "P0"},
            ]},
            {"name": "智能预算分配", "icon": "Bd", "status": "todo", "features": [
                {"f": "基于CPI/ROAS的预算自动分配算法", "p": "P1"},
                {"f": "跨渠道预算比例优化", "p": "P2"},
                {"f": "预算爬坡自动化(每日上限20%)", "p": "P1"},
                {"f": "预算预警(消耗速度异常/超预算池上限)", "p": "P0"},
            ]},
            {"name": "异常检测", "icon": "Al", "status": "todo", "features": [
                {"f": "花费突增/骤降检测(超均值±50% → 告警)", "p": "P0"},
                {"f": "CPI暴涨检测(>基准×1.5且spend>$100)", "p": "P0"},
                {"f": "素材审核拒绝追踪(被拒>3次 → 标记通知)", "p": "P1"},
                {"f": "Learning Phase 保护(创建<3天不执行自动调整)", "p": "P0"},
            ]},
        ]},
        {"name": "基础设施层", "color": "#8c8c8c", "desc": "用户权限、任务调度、监控告警等基础支撑能力", "modules": [
            {"name": "用户与权限", "icon": "Us", "status": "todo", "features": [
                {"f": "角色体系(Admin/Lead/Optimizer/Viewer/Finance)", "p": "P0"},
                {"f": "操作审计日志(所有写操作记录)", "p": "P0"},
                {"f": "敏感操作审批(大额预算调整需主管审批)", "p": "P1"},
                {"f": "Token 加密存储(AES-256, 不在日志暴露)", "p": "P0"},
                {"f": "多租户数据隔离(tenant_id)", "p": "P1"},
            ]},
            {"name": "任务调度", "icon": "Ts", "status": "todo", "features": [
                {"f": "定时任务(报表拉取/规则执行/Token刷新)", "p": "P0"},
                {"f": "异步任务队列(批量操作/大规模创编)", "p": "P0"},
                {"f": "任务重试与死信队列", "p": "P1"},
                {"f": "任务状态可视化监控", "p": "P2"},
            ]},
            {"name": "监控与告警", "icon": "Mo", "status": "todo", "features": [
                {"f": "API调用成功率/延迟监控", "p": "P0"},
                {"f": "平台限流告警(接近限流阈值 → 告警)", "p": "P0"},
                {"f": "服务健康检查", "p": "P1"},
                {"f": "业务指标异常告警(花费/CPI/ROAS)", "p": "P0"},
            ]},
        ]},
    ],
    "data_flows": [
        {"from": "广告投放层", "to": "平台对接层", "label": "统一API调用(创编/修改/查询)"},
        {"from": "平台对接层", "to": "广告平台", "label": "Meta/Google/TikTok/AppLovin API"},
        {"from": "广告平台", "to": "数据与归因层", "label": "Reporting API + MMP回传"},
        {"from": "数据与归因层", "to": "智能化层", "label": "指标数据驱动规则评估"},
        {"from": "智能化层", "to": "广告投放层", "label": "自动调整(预算/出价/启停)"},
    ],
    "build_phases": [
        {"phase": "Phase 1: 地基搭建", "duration": "2-3周", "color": "#389e0d", "modules": [
            "平台账户管理", "应用管理", "统一Connector(Meta+Google)"
        ], "goal": "能绑定Meta和Google账户，Token安全存储，基础API调通"},
        {"phase": "Phase 2: 核心投放链路", "duration": "3-4周", "color": "#36cfc9", "modules": [
            "广告创编", "广告模板", "字段映射引擎", "素材管理(上传+校验)"
        ], "goal": "能通过平台完成Meta+Google的完整创编流程"},
        {"phase": "Phase 3: 数据闭环", "duration": "2-3周", "color": "#ff7a45", "modules": [
            "归因数据接入(AppsFlyer)", "数据报表", "数据仓库(PostgreSQL+ETL)"
        ], "goal": "能看到完整的投放数据报表，花费-安装-CPI闭环"},
        {"phase": "Phase 4: 运营效率", "duration": "2-3周", "color": "#b37feb", "modules": [
            "广告运营(批量操作)", "规则引擎", "异常检测", "渠道返点管理"
        ], "goal": "优化师日常运营效率工具，规则引擎替代人工盯盘"},
        {"phase": "Phase 5: 智能化进阶", "duration": "3-4周", "color": "#eb2f96", "modules": [
            "智能预算分配", "Cohort/LTV分析", "A/B Test", "TikTok+AppLovin Connector"
        ], "goal": "智能化自动投放，数据驱动决策闭环"},
        {"phase": "Phase 6: 企业级能力", "duration": "2-3周", "color": "#8c8c8c", "modules": [
            "用户与权限", "多租户隔离", "监控与告警", "任务调度可视化"
        ], "goal": "多团队协作，安全合规，生产级稳定性"},
    ],
}

PLATFORM_COMPARISON = {
    "title": "广告平台能力对比",
    "dimensions": ["API版本", "广告结构", "最低日预算", "出价策略", "素材类型", "数据延迟", "API限流"],
    "platforms": [
        {"name": "Meta", "icon": "M", "color": "#1877f2",
         "values": ["v21.0", "Campaign→Ad Set→Ad", "$1", "Lowest Cost/Cost Cap/Bid Cap/Min ROAS",
                    "图片/视频/轮播/Playable", "15-30min", "200写/小时/账户"]},
        {"name": "TikTok", "icon": "T", "color": "#000000",
         "values": ["v1.3", "Campaign→Ad Group→Ad", "$20", "Lowest Cost/Cost Cap",
                    "视频/图片/Playable/Spark Ads", "1-3h", "10 QPS/App"]},
        {"name": "Google Ads", "icon": "G", "color": "#4285f4",
         "values": ["v18", "Campaign→Ad Group→Ad", "$1", "Max Conv/Target CPA/Target ROAS/Max Clicks",
                    "图片/视频/HTML5/App开屏", "3-6h", "15000请求/天"]},
        {"name": "AppLovin", "icon": "A", "color": "#194e8b",
         "values": ["Mgmt API v1", "Campaign→Ad Group→Ad", "$100", "Target CPI/CPA/ROAS",
                    "视频/Playable/Banner/Rewarded", "2-4h", "~5 QPS建议"]},
    ],
}

MODULES = [
    {
        "id": "platform_meta", "name": "Meta Marketing API", "layer": "平台集成",
        "icon": "M", "color": "#1877f2",
        "summary": "Facebook/Instagram广告API，全球最大社交广告平台",
        "api_version": "v21.0 → v25.0推进中", "doc_url": "https://developers.facebook.com/docs/marketing-apis",
        "key_points": [
            {"label": "广告结构", "value": "Campaign → Ad Set → Ad 三层"},
            {"label": "认证方式", "value": "BM → System User → Long-lived Token(60天刷新)"},
            {"label": "核心权限", "value": "ads_management / ads_read / business_management"},
            {"label": "API限流", "value": "~200次写操作/小时/账户，Batch API最多50个/批"},
            {"label": "最低预算", "value": "日预算$1起"},
            {"label": "Advantage+", "value": "v23.0+ 受众默认开启，v25.0 统一Advantage+架构(废弃smart_promotion_type)"},
        ],
        "capabilities": [
            {"title": "广告管理颗粒度", "items": [
                "Campaign层：目标(OUTCOME_APP_PROMOTION / TRAFFIC / ENGAGEMENT / LEADS / SALES)、特殊广告类别、CBO开关",
                "Ad Set层：地区/年龄/性别/兴趣/自定义受众/Lookalike、版位(Facebook/Instagram/Audience Network/Messenger的Feed/Stories/Reels等)、优化目标(APP_INSTALLS/CONVERSIONS/VALUE)、出价策略(LOWEST_COST/COST_CAP/BID_CAP/MINIMUM_ROAS)、预算/排期",
                "Ad层：素材(图片/视频/轮播/Playable)、标题/正文/描述、CTA、追踪链接(Deep Link)、UTM参数、DCO开关",
            ]},
            {"title": "接入要点", "items": [
                "素材上传：POST /act_{id}/adimages 或 /advideos → 获取hash/video_id → 绑定Ad Creative",
                "Dry-run：创建时 validation_only=true 预校验",
                "异步操作：大批量用 Async Requests(POST /act_{id}/asyncadrequestsets)，轮询状态",
                "Webhook：可订阅 Ad Account 变更通知(leads/ad_status等)",
            ]},
            {"title": "报表能力", "items": [
                "Insights API：GET /{object_id}/insights，支持 date_preset/time_range/time_increment",
                "Breakdown：age/gender/country/publisher_platform/platform_position/device_platform",
                "核心指标：spend/impressions/clicks/cpc/cpm/ctr/actions/cost_per_action_type/action_values",
                "数据延迟：实时约15-30min，归因窗口内数据持续回溯修正(最长28天)",
            ]},
        ],
        "config_chain_key": "meta",
    },
    {
        "id": "platform_tiktok", "name": "TikTok Business API", "layer": "平台集成",
        "icon": "T", "color": "#000000",
        "summary": "TikTok广告API，全球增长最快的短视频广告平台",
        "api_version": "v1.3", "doc_url": "https://business-api.tiktok.com/portal/docs",
        "key_points": [
            {"label": "广告结构", "value": "Campaign → Ad Group → Ad 三层"},
            {"label": "认证方式", "value": "App ID + Secret → OAuth → Long-lived Token(1年)"},
            {"label": "API限流", "value": "10 QPS/App，写操作建议 ≤5 QPS"},
            {"label": "最低预算", "value": "日预算$20起"},
            {"label": "特色能力", "value": "Spark Ads(原生视频授权)、ACO(自动创意优化)"},
        ],
        "capabilities": [
            {"title": "广告管理颗粒度", "items": [
                "Campaign层：目标(APP_INSTALL/CONVERSIONS/TRAFFIC/REACH/VIDEO_VIEWS/LEAD_GENERATION/PRODUCT_SALES)、预算模式(日/总/不限)、CBO",
                "Ad Group层：版位(TikTok/Pangle/Global App Bundle)、定向(location/age/gender/language/interest/behavior/device/OS)、出价策略(Lowest Cost/Cost Cap)、Day-parting",
                "Ad层：素材(视频/图片/Playable/Spark Ads)、标题(≤100字符)、CTA、追踪URL(Impression/Click)、Identity(Spark Ads需授权码)",
            ]},
            {"title": "接入要点", "items": [
                "素材上传：POST /file/video/ad/upload(≤500MB)或 /file/image/ad/upload → video_id/image_id",
                "批量创建：单次最多20个Campaign/Ad Group/Ad",
                "Spark Ads：需创作者授权码(Authorization Code)，有效期30/60/365天",
                "Smart Creative(ACO)：系统自动组合多素材多标题，找到最优组合",
            ]},
            {"title": "报表能力", "items": [
                "Reporting API：POST /report/integrated/get，支持BASIC/AUDIENCE/PLAYABLE_MATERIAL",
                "维度：stat_time_day/campaign_id/adgroup_id/ad_id/country_code/platform",
                "指标：spend/impressions/clicks/ctr/cpc/cpm/conversion/cost_per_conversion/skan_conversion",
                "数据延迟：约1-3小时，SKAN数据延迟24-72小时",
            ]},
        ],
    },
    {
        "id": "platform_google", "name": "Google Ads API", "layer": "平台集成",
        "icon": "G", "color": "#4285f4",
        "summary": "全球最大的搜索和展示广告平台，覆盖Search/Display/YouTube/UAC",
        "api_version": "v18 (2025)", "doc_url": "https://developers.google.com/google-ads/api/docs/start",
        "key_points": [
            {"label": "广告结构", "value": "Campaign → Ad Group → Ad/Asset Group(PMax)"},
            {"label": "认证方式", "value": "OAuth 2.0 + Developer Token + MCC Account"},
            {"label": "API限流", "value": "15,000 requests/day(Basic)，可申请Standard提升"},
            {"label": "最低预算", "value": "日预算$1起(UAC建议≥$50即≥10×CPI)"},
            {"label": "特色能力", "value": "UAC全自动化(不支持手动版位/定向)、Performance Max跨渠道、Smart Bidding"},
            {"label": "自动化程度", "value": "App Campaign高度自动化：素材是唯一可控杠杆，版位/定向/出价全ML控制"},
        ],
        "capabilities": [
            {"title": "广告管理颗粒度", "items": [
                "Campaign层：类型(SEARCH/DISPLAY/VIDEO/APP/PERFORMANCE_MAX/DEMAND_GEN)、预算(日预算/共享预算)、出价策略、地区/语言、网络设置",
                "Ad Group层(非UAC)：关键词/受众/展示定向、出价、广告轮播设置",
                "Ad层：文字广告(标题×15+描述×4)/图片/视频/HTML5/响应式广告",
                "UAC(App Campaign)：高度自动化，只需提供素材+文案+出价+预算，Google自动分配Search/Display/YouTube/Play",
            ]},
            {"title": "接入要点", "items": [
                "认证流程：Google Cloud Project → 启用Google Ads API → 申请Developer Token → OAuth 2.0客户端 → Refresh Token",
                "Manager Account(MCC)：管理多个广告账户的层级结构，API操作需指定 customer_id 和 login-customer-id(MCC ID)",
                "GAQL查询：Google Ads Query Language(类SQL)查询资源和报表，替代旧版报表下载",
                "Mutate操作：通过 GoogleAdsService.Mutate 批量创建/修改资源，单次最多5000个操作",
                "Conversion Tracking：需要在账户中配置Conversion Action，关联Firebase/MMP回传",
                "Change Status：使用 campaign.status = PAUSED/ENABLED 控制启停",
            ]},
            {"title": "报表能力", "items": [
                "GAQL报表：SELECT metrics.cost_micros, metrics.impressions... FROM campaign WHERE segments.date DURING LAST_7_DAYS",
                "维度(segments)：date/device/ad_network_type/conversion_action/geo_target_country 等",
                "核心指标(metrics)：cost_micros/impressions/clicks/conversions/conversions_value/ctr/average_cpc/cost_per_conversion",
                "数据延迟：Search约3小时，Display/YouTube约6小时，Conversion数据可能延迟24-72小时",
                "Change History：可查询账户所有变更记录(类似审计日志)",
            ]},
        ],
        "config_chain_key": "google",
    },
    {
        "id": "platform_applovin", "name": "AppLovin", "layer": "平台集成",
        "icon": "A", "color": "#194e8b",
        "summary": "移动应用广告平台，擅长App Install和应用内变现",
        "api_version": "Management API v1",
        "doc_url": "https://dash.applovin.com/documentation/mediation/api",
        "key_points": [
            {"label": "广告结构", "value": "Campaign → Ad Group → Ad(简化结构)"},
            {"label": "认证方式", "value": "Management API Key(Dashboard → Settings → Keys)"},
            {"label": "最低预算", "value": "日预算$100起"},
            {"label": "自动化程度", "value": "定向高度自动化，人工干预颗粒度较粗"},
            {"label": "特色能力", "value": "Axon(自有归因系统，2024年推出)"},
        ],
        "capabilities": [
            {"title": "广告管理颗粒度", "items": [
                "Campaign层：类型(UA/Retargeting/Brand)、日预算(≥$100)、目标CPI/CPA/ROAS",
                "Ad Group层：国家/设备类型/OS版本、Day-parting(定向高度依赖算法)",
                "Ad层：视频/Playable/Banner/Interstitial/Rewarded、尺寸(16:9/9:16/1:1)、End Card",
            ]},
            {"title": "接入要点", "items": [
                "创建Campaign：POST /campaign/api/create，必须关联app package/bundle ID",
                "素材管理：通过Creative API上传Video/Playable HTML/Image",
                "Axon归因：AppLovin自有归因系统，替代传统MMP，在AppLovin生态内完成归因",
                "限流宽松，建议控制在5 QPS以内",
            ]},
            {"title": "报表能力", "items": [
                "Reporting API：GET /report，支持 campaign/country/creative/platform/day 维度",
                "指标：impressions/clicks/installs/ctr/cvr/cpi/spend/ecpm/revenue",
                "Cohort Report：按安装日期查看D1/D3/D7 retention和LTV",
                "数据延迟：约2-4小时，Axon归因数据更实时；格式CSV/JSON",
            ]},
        ],
    },
    {
        "id": "mmp_appsflyer", "name": "AppsFlyer", "layer": "归因与数据",
        "icon": "AF", "color": "#4ecb71",
        "summary": "全球最大移动归因平台，覆盖Install/Event/Revenue/SKAN",
        "api_version": "Pull API v2 / S2S",
        "doc_url": "https://support.appsflyer.com/hc/en-us/categories/201114756-API",
        "key_points": [
            {"label": "归因类型", "value": "Click-through(7天) / View-through(1天) / SKAN / Probabilistic"},
            {"label": "数据获取", "value": "Push(实时Callback) + Pull(批量API) + S2S(事件上报)"},
            {"label": "反作弊", "value": "Protect360(Device Farm/Click Flooding/SDK Spoofing识别)"},
            {"label": "数据保留", "value": "原始数据90天(可付费延长)，聚合数据永久"},
            {"label": "追踪链接", "value": "OneLink(Deep Link / Deferred Deep Link / Universal Link)"},
        ],
        "capabilities": [
            {"title": "归因能力详解", "items": [
                "Click-through：点击后安装，归因窗口默认7天(可配1-30天)",
                "View-through：曝光后安装，窗口默认1天(可配1-48小时)",
                "SKAN(iOS)：基于SKAdNetwork 4.0，支持Coarse/Fine Conversion Value，延迟24-72小时",
                "Re-engagement/Re-attribution：卸载重装或Deep Link唤醒归因",
                "Probabilistic Modeling：无IDFA场景概率归因(准确率约85-90%)",
            ]},
            {"title": "数据获取方式", "items": [
                "Pull API(批量)：GET /api/v2/export/app/{app_id}/installs_report，按天拉取CSV/JSON",
                "Push API(实时)：配置Callback URL，每次Install/Event秒级推送Postback",
                "S2S Events：POST api2.appsflyer.com/inappevent/{app_id}，从服务器上报In-App Event",
                "Master API：聚合报表(media_source/campaign/adset/ad/geo/date)",
                "Cohort API：安装日期分组，D1-D365留存/LTV/Revenue",
            ]},
            {"title": "接入要点", "items": [
                "API Token：Dashboard → API Access 获取V2 Token",
                "SDK集成：客户端集成AF SDK(Android/iOS)，配置App ID + Dev Key",
                "标准事件：af_purchase/af_level_achieved/af_tutorial_completion + 自定义事件",
                "OneLink：追踪链接系统，支持Deep Link/Deferred Deep Link/Universal Link",
            ]},
        ],
    },
    {
        "id": "mmp_adjust", "name": "Adjust", "layer": "归因与数据",
        "icon": "Ad", "color": "#0a8ce3",
        "summary": "全球第二大移动归因平台，以简洁和隐私合规著称",
        "api_version": "API v2",
        "doc_url": "https://help.adjust.com/en/developer/api",
        "key_points": [
            {"label": "归因类型", "value": "Click(7天) / Impression(24h) / Fingerprint(24h) / SKAN"},
            {"label": "数据获取", "value": "Callback(实时推送,100+宏参数) + Pull API(聚合) + CSV Export"},
            {"label": "反作弊", "value": "Fraud Prevention(Click Injection/SDK Spoofing检测)"},
            {"label": "隐私合规", "value": "GDPR Forget Device API / COPPA合规"},
            {"label": "Partner集成", "value": "内置Meta/TikTok/Google/Unity等Module，直接启用"},
        ],
        "capabilities": [
            {"title": "归因能力详解", "items": [
                "Click归因窗口：默认7天(可配1-30天)，Fingerprint归因24小时",
                "Impression归因窗口：默认24小时",
                "SKAN：4.0 Conversion Value映射，支持Fine/Coarse粒度",
                "Reattribution：卸载后重装归因，窗口可配",
                "S2S归因：适用于PC/Console/CTV等非移动场景",
            ]},
            {"title": "数据获取方式", "items": [
                "Callback(实时)：配置URL，每次Install/Event/Session实时推送，100+宏参数",
                "Pull API(聚合)：GET /kpis/v1/{app_token} 拉取聚合KPI",
                "CSV Export：原始数据导出(Install/Event/Session/Click/Impression)，按天可用",
                "Datascape API：新版分析API，自定义维度和指标组合",
            ]},
            {"title": "接入要点", "items": [
                "认证：App Token + API Token(Dashboard获取)",
                "Tracker：每个渠道/Campaign创建Tracker URL(Click URL + Impression URL)",
                "事件Token：每种In-App Event创建Event Token(6位字符串)",
                "Partner Module：主流平台有内置集成，直接启用即可",
            ]},
        ],
    },
    {
        "id": "creative_mgmt", "name": "素材管理", "layer": "业务能力",
        "icon": "Cr", "color": "#fa8c16",
        "summary": "素材全生命周期：上传→规格校验→平台分发→效果分析→疲劳监控",
        "key_points": [
            {"label": "核心流程", "value": "上传 → 规格校验 → 标签分类 → 平台分发 → 效果追踪 → 疲劳替换"},
            {"label": "支持格式", "value": "图片/视频/轮播/Playable HTML/End Card"},
            {"label": "智能能力", "value": "自动裁剪(16:9/9:16/1:1)、效果评分、疲劳度监控"},
        ],
        "capabilities": [
            {"title": "各平台素材规格对比", "items": [
                "Meta：图片(1080×1080/1200×628/1080×1920)≤30MB、视频(≤240s推荐15s,H.264,≤4GB)、轮播(2-10张)、Playable(≤2MB)",
                "TikTok：视频(9:16为主,≥540×960,6-60s推荐9-15s,≤500MB)、图片(1200×628/720×1280)、Spark Ads",
                "Google：图片(1200×628/300×250等)、视频(YouTube格式,推荐15-30s)、HTML5(≤150KB)、App开屏",
                "AppLovin：视频(16:9/9:16/1:1,15-30s,H.264,≤100MB)、Playable(HTML5,≤5MB)、End Card(800×600)、Banner(320×50/300×250)",
            ]},
            {"title": "核心功能", "items": [
                "素材库：标签分类(游戏/地区/语言/风格)、搜索过滤、版本管理(A/B Test)",
                "规格校验：上传时自动检测分辨率/时长/大小/编码，对比目标平台要求",
                "智能裁剪：同一视频自动生成16:9/9:16/1:1三种比例",
                "效果看板：每个素材CTR/CVR/CPI/IPM趋势图，跨平台对比，Top排行",
                "疲劳监控：CTR连续N天下降或IPM低于阈值 → 推荐替换",
            ]},
        ],
    },
    {
        "id": "campaign_mgmt", "name": "广告管理", "layer": "业务能力",
        "icon": "Ca", "color": "#36cfc9",
        "summary": "Campaign三层结构管理，跨平台创编/模板复用/批量操作",
        "key_points": [
            {"label": "创编流程", "value": "6步向导：目标→预算→定向→出价→素材→预览提交"},
            {"label": "跨平台", "value": "统一数据模型→各平台字段映射→规格自动适配"},
            {"label": "效率工具", "value": "Campaign模板/定向模板/素材组模板/批量操作/命名规则"},
        ],
        "capabilities": [
            {"title": "投放目标体系", "items": [
                "App Install(CPI)：最常见UA目标，优化安装成本",
                "AEO(App Event)：优化应用内事件(注册/付费/关卡)，需MMP事件回传",
                "VO(Value)：优化付费金额，需Purchase+Revenue回传，适合成熟产品",
                "Traffic/Clicks：引导访问落地页/商店页，按CPC优化",
                "Reach/Impressions：最大化覆盖人数，品牌广告",
                "Video Views：优化视频观看(ThruPlay)，品牌曝光",
                "Lead Generation：收集用户信息(Email/Phone)，B2B/订阅制",
            ]},
            {"title": "跨平台差异处理", "items": [
                "字段映射：统一模型→各平台API字段(bid_strategy在Meta是BID_CAP/TikTok是BID_TYPE_CUSTOM/Google是TARGET_CPA)",
                "目标映射：APP_INSTALL→Meta OUTCOME_APP_PROMOTION / TikTok APP_INSTALL / Google APP_CAMPAIGN",
                "预算差异：Meta $1/天、TikTok $20/天、AppLovin $100/天、Google建议≥$50",
                "版位映射：统一版位名→各平台placement ID",
                "素材适配：同一素材按目标平台自动裁剪/转码",
            ]},
            {"title": "模板体系", "items": [
                "Campaign模板：完整创编配置(目标/预算/定向/出价/素材/文案)一键复用",
                "定向模板：常用地区+受众组合(如'T1-iOS-Core'/'SEA-Android-Broad')",
                "素材组模板：素材+文案+CTA固定组合，标准化广告单元",
                "命名规则：自动生成 {App}_{Geo}_{Obj}_{Date}_{Ver} 格式",
            ]},
        ],
    },
    {
        "id": "data_system", "name": "标准数据", "layer": "业务能力",
        "icon": "Da", "color": "#ff7a45",
        "summary": "多维实时报表、核心KPI指标体系、归因数据融合",
        "key_points": [
            {"label": "指标体系", "value": "Spend/Impressions/Clicks/Installs/CPI/CTR/CVR/IPM/ROAS/pLTV"},
            {"label": "报表维度", "value": "时间/平台/地区/应用/Campaign层级/素材/设备"},
            {"label": "数据融合", "value": "以MMP归因数据为准，关联平台Spend计算衍生指标"},
        ],
        "capabilities": [
            {"title": "核心指标体系", "items": [
                "花费类：Spend / Budget Utilization / Spend Velocity",
                "曝光类：Impressions / Reach / Frequency / CPM",
                "点击类：Clicks / CTR / CPC",
                "转化类：Installs / CVR / CPI / IPM(千次展示安装数)",
                "深度事件：Registration/Purchase/Level等 / CPA",
                "收入类：Revenue / ROAS / pLTV / Payback Period",
            ]},
            {"title": "数据融合与延迟", "items": [
                "平台数据(Spend/Impression/Click)：各平台Reporting API拉取，15min-6h延迟",
                "归因数据(Install/Event/Revenue)：MMP Callback实时推送或Pull API批量拉取",
                "融合逻辑：MMP归因为准，关联平台Spend，计算CPI/ROAS等衍生指标",
                "数据回溯：归因窗口内持续修正(Meta最长28天)，需支持回刷机制",
                "SKAN特殊处理：延迟24-72h、Campaign粒度、Conversion Value解码映射",
            ]},
        ],
    },
    {
        "id": "rule_engine", "name": "规则引擎", "layer": "智能化",
        "icon": "Ru", "color": "#b37feb",
        "summary": "条件+动作的自动化规则，替代人工盯盘，7×24自动执行",
        "key_points": [
            {"label": "规则类型", "value": "止损/加量/素材替换/预算预警/异常检测/Learning Phase保护"},
            {"label": "触发机制", "value": "定时(每小时/4小时/每天) 或 事件触发(数据更新时)"},
            {"label": "安全机制", "value": "冷却期/人工审批/Learning Phase保护/执行日志审计"},
        ],
        "capabilities": [
            {"title": "典型规则示例", "items": [
                "止损：CPI > 目标×1.3 且 消耗>$50 → 暂停Ad Set",
                "零转化止损：消耗>$30 且 Install=0 → 暂停Ad Set",
                "加量：CPI < 目标×0.8 且 消耗>$100 且 运行>2天 → 预算+20%",
                "ROAS优化：D7 ROAS > 目标×1.2 → 预算+30%",
                "素材疲劳：CTR连续3天下降且 < 首日×0.7 → 暂停素材",
                "异常检测：消耗突增/骤降超均值±50% → 告警",
                "Learning保护：创建<3天且转化<50 → 不执行自动调整",
            ]},
            {"title": "引擎设计", "items": [
                "条件组合：AND/OR逻辑 + >/</>=/<=/ =/!= 比较运算符",
                "时间窗口：当天/近3天/近7天，避免基于瞬时数据决策",
                "冷却期：调整后N小时内不再触发同类规则",
                "执行模式：自动执行 / 人工审批(高风险操作如暂停Campaign)",
                "日志审计：每次触发记录时间/对象/条件值/动作/结果",
            ]},
        ],
    },
    {
        "id": "template_system", "name": "模板与效率", "layer": "效率工具",
        "icon": "Te", "color": "#eb2f96",
        "summary": "模板化+批量操作提升优化师工作效率，沉淀最佳实践",
        "key_points": [
            {"label": "模板类型", "value": "Campaign模板/定向模板/素材组模板/命名规则模板"},
            {"label": "批量操作", "value": "启停/调预算/复制/跨平台上线/Excel导入"},
        ],
        "capabilities": [
            {"title": "模板体系", "items": [
                "Campaign模板：完整创编配置一键复用",
                "定向模板：T1-iOS-Core / SEA-Android-Broad 等常用组合",
                "素材组模板：素材+文案+CTA固定搭配",
                "命名规则：{App}_{Geo}_{Obj}_{Date}_{Ver} 自动生成",
            ]},
            {"title": "批量操作", "items": [
                "批量启停：一键暂停/开启多个Campaign/Ad Set",
                "批量调预算：按比例或按金额批量调整",
                "批量复制：复制到其他地区/平台(仅改定向/预算)",
                "跨平台上线：同一素材同时推送Meta/TikTok/Google/AppLovin",
                "Excel导入：模板批量创建Campaign(大规模拓量)",
            ]},
        ],
    },
    {
        "id": "user_system", "name": "用户与权限", "layer": "基础设施",
        "icon": "Us", "color": "#8c8c8c",
        "summary": "多角色权限控制、操作审计、多租户隔离",
        "key_points": [
            {"label": "角色体系", "value": "Admin/Lead/Optimizer/Viewer/Finance 五种角色"},
            {"label": "安全机制", "value": "操作审计日志/敏感操作审批/Token加密存储/多租户隔离"},
        ],
        "capabilities": [
            {"title": "角色权限", "items": [
                "管理员(Admin)：全局配置、用户管理、平台账户绑定",
                "主管(Lead)：所有数据查看、规则审批、预算审批、团队管理",
                "优化师(Optimizer)：创编/调整/素材/规则(限本人Campaign)",
                "只读(Viewer)：仅查看报表数据",
                "财务(Finance)：花费数据/预算审批/账单管理",
            ]},
            {"title": "安全审计", "items": [
                "审计日志：所有写操作记录操作人/时间/变更内容",
                "敏感操作审批：删除Campaign/大额预算调整(>$1000/天)需主管审批",
                "Token安全：Access Token AES-256加密存储，不在日志/前端暴露",
                "多租户：数据按tenant_id物理隔离",
            ]},
        ],
    },
]

LAYERS_ORDER = ["平台集成", "归因与数据", "业务能力", "智能化", "效率工具", "基础设施"]
LAYER_COLORS = {
    "平台集成": "#e6f4ff", "归因与数据": "#e8f5e9", "业务能力": "#fff3e0",
    "智能化": "#f3e5f5", "效率工具": "#fce4ec", "基础设施": "#f5f5f5",
}
LAYER_DESCS = {
    "平台集成": "统一对接各广告平台Open API，屏蔽平台差异，提供标准化操作接口",
    "归因与数据": "对接MMP归因平台，获取Install/Event/Revenue数据，支撑效果衡量",
    "业务能力": "优化师日常核心操作：素材管理、广告创编、数据报表",
    "智能化": "规则引擎自动化盯盘，减少人工操盘，提升响应速度",
    "效率工具": "模板化+批量操作提升效率，沉淀最佳实践",
    "基础设施": "用户权限、安全审计等基础支撑",
}


CHANNEL_CONFIGS = {
    "meta": {
        "platform": "Meta", "icon": "M", "color": "#1877f2",
        "api_version": "v21.0 (v22.0+ 推进中, v25.0 将统一 Advantage+)",
        "last_updated": "2025-06",
        "creation_flow": [
            {"step": 1, "name": "Campaign层", "fields": [
                {"field": "objective", "label": "投放目标", "type": "select", "required": True,
                 "options": ["OUTCOME_APP_PROMOTION", "OUTCOME_TRAFFIC", "OUTCOME_ENGAGEMENT", "OUTCOME_LEADS", "OUTCOME_SALES", "OUTCOME_AWARENESS"],
                 "note": "v21.0起统一为OUTCOME_前缀，旧目标(APP_INSTALLS等)自动映射"},
                {"field": "special_ad_categories", "label": "特殊广告类别", "type": "multi_select", "required": True,
                 "options": ["NONE", "HOUSING", "EMPLOYMENT", "CREDIT", "ISSUES_ELECTIONS_POLITICS"],
                 "note": "若选非NONE，定向将受限(不能按年龄/性别/ZIP Code精确定向)"},
                {"field": "campaign_budget_optimization", "label": "CBO (Campaign Budget Optimization)", "type": "toggle", "required": False,
                 "note": "开启后预算在Campaign层统一管理，系统自动分配给各Ad Set"},
                {"field": "daily_budget / lifetime_budget", "label": "Campaign预算", "type": "number", "required": "CBO开启时必填",
                 "note": "日预算最低$1/天，总预算需设置结束日期"},
                {"field": "buying_type", "label": "购买类型", "type": "select", "required": False,
                 "options": ["AUCTION", "RESERVED"],
                 "note": "绝大多数选AUCTION竞价，RESERVED仅品牌广告"},
                {"field": "bid_strategy", "label": "出价策略(Campaign级)", "type": "select", "required": False,
                 "options": ["LOWEST_COST_WITHOUT_CAP", "COST_CAP", "BID_CAP", "MINIMUM_ROAS"],
                 "note": "CBO开启时在此设置；LOWEST_COST不设上限让Meta自动优化"},
                {"field": "advantage_campaign_budget", "label": "Advantage+ Campaign Budget", "type": "auto",
                 "note": "v25.0起，配合Advantage+受众和版位自动进入Advantage+状态，无需smart_promotion_type标志"},
            ]},
            {"step": 2, "name": "Ad Set层", "fields": [
                {"field": "optimization_goal", "label": "优化目标", "type": "select", "required": True,
                 "options": ["APP_INSTALLS", "OFFSITE_CONVERSIONS", "VALUE", "LINK_CLICKS", "LANDING_PAGE_VIEWS", "REACH", "IMPRESSIONS", "THRUPLAY", "LEAD_GENERATION"],
                 "note": "需与Campaign objective匹配，如APP_PROMOTION配APP_INSTALLS或OFFSITE_CONVERSIONS"},
                {"field": "billing_event", "label": "计费事件", "type": "select", "required": True,
                 "options": ["IMPRESSIONS", "LINK_CLICKS", "APP_INSTALLS", "THRUPLAY"],
                 "note": "大多数目标默认IMPRESSIONS(oCPM)"},
                {"field": "targeting.geo_locations", "label": "地区定向", "type": "multi_select", "required": True,
                 "note": "必填，支持国家/地区/城市/ZIP Code/GPS半径，Advantage+不会扩展此项"},
                {"field": "targeting.age_min / age_max", "label": "年龄范围", "type": "range", "required": False,
                 "note": "默认18-65，Advantage+开启时作为建议范围(系统可扩展)"},
                {"field": "targeting.genders", "label": "性别", "type": "select",
                 "options": ["All(0)", "Male(1)", "Female(2)"],
                 "note": "默认All，Advantage+开启时作为建议"},
                {"field": "targeting.flexible_spec", "label": "兴趣/行为定向", "type": "multi_select", "required": False,
                 "note": "兴趣(interests)、行为(behaviors)、人口统计(demographics)，Advantage+会自动扩展"},
                {"field": "targeting.custom_audiences", "label": "自定义受众", "type": "multi_select", "required": False,
                 "note": "CRM上传/网站访客/App用户/Lookalike，Advantage+会将其作为建议信号"},
                {"field": "targeting_automation.advantage_audience", "label": "Advantage+ 受众", "type": "toggle",
                 "note": "【关键】v23.0起新Ad Set默认开启=1，系统自动扩展定向以获取更多转化。关闭=0需显式设置。兴趣/自定义受众变为建议信号而非硬约束"},
                {"field": "publisher_platforms", "label": "版位平台", "type": "multi_select",
                 "options": ["facebook", "instagram", "audience_network", "messenger"],
                 "note": "Advantage+版位 = 全选(推荐)，让Meta自动分配"},
                {"field": "facebook_positions", "label": "Facebook版位", "type": "multi_select",
                 "options": ["feed", "right_hand_column", "instant_article", "marketplace", "video_feeds", "stories", "reels", "search", "in_stream_video"],
                 "note": "选Automatic让Meta自动选择版位(推荐)"},
                {"field": "instagram_positions", "label": "Instagram版位", "type": "multi_select",
                 "options": ["stream", "story", "reels", "explore", "explore_home", "profile_feed", "ig_search"],
                 "note": "选Automatic时系统自动分配"},
                {"field": "bid_amount", "label": "出价金额", "type": "number", "required": "COST_CAP/BID_CAP时必填",
                 "note": "COST_CAP: 平均成本上限; BID_CAP: 每次竞价最高出价; MINIMUM_ROAS: 最低回报率"},
                {"field": "daily_budget / lifetime_budget", "label": "Ad Set预算", "type": "number", "required": "CBO关闭时必填",
                 "note": "CBO关闭时在Ad Set层设置预算，最低$1/天"},
                {"field": "start_time / end_time", "label": "排期", "type": "datetime", "required": True,
                 "note": "start_time必填，end_time选填(总预算时必填)，ISO 8601格式"},
                {"field": "promoted_object", "label": "推广对象", "type": "object", "required": "App类目标必填",
                 "note": "App类目标需填application_id + object_store_url(商店链接) + custom_event_type(AEO/VO时)"},
                {"field": "attribution_spec", "label": "归因窗口", "type": "object",
                 "note": "默认7天点击+1天曝光，可配: click_window=1/7/28天, view_window=0/1天"},
            ]},
            {"step": 3, "name": "Ad层", "fields": [
                {"field": "creative", "label": "广告创意", "type": "object", "required": True,
                 "note": "需先通过/act_{id}/adcreatives创建Creative对象，获取creative_id"},
                {"field": "creative.image_hash / video_id", "label": "素材", "type": "upload",
                 "note": "图片: POST /act_{id}/adimages → hash; 视频: POST /act_{id}/advideos → video_id"},
                {"field": "creative.title / body / description", "label": "文案", "type": "text",
                 "note": "title: ≤40字符; body(primary text): ≤125字符建议; description: ≤30字符"},
                {"field": "creative.call_to_action_type", "label": "CTA按钮", "type": "select",
                 "options": ["INSTALL_MOBILE_APP", "LEARN_MORE", "SIGN_UP", "SHOP_NOW", "PLAY_GAME", "DOWNLOAD", "BOOK_TRAVEL", "SUBSCRIBE", "GET_OFFER"],
                 "note": "App类目标常用INSTALL_MOBILE_APP"},
                {"field": "creative.link_data.link", "label": "落地页/商店链接", "type": "url", "required": True,
                 "note": "App类填商店链接，网页类填落地页URL"},
                {"field": "creative.url_tags", "label": "UTM追踪参数", "type": "text",
                 "note": "自动追加到链接: utm_source=facebook&utm_campaign={{campaign.name}}等"},
                {"field": "tracking_specs", "label": "追踪设置", "type": "object",
                 "note": "关联MMP追踪链接，如AppsFlyer/Adjust的Click URL"},
                {"field": "advantage_creative_enhancements", "label": "Advantage+ 创意增强", "type": "multi_toggle",
                 "note": "【v22.0+新】个别增强项可独立开关: image_templates/text_optimizations/inline_comment/music/image_touchups等，取代旧的standard_enhancements捆绑"},
            ]},
        ],
        "smart_features": [
            {"name": "Advantage+ Campaign", "desc": "同时开启Advantage+预算+受众+版位，系统全自动优化分配，适合ASC(App)和AAC场景", "recommendation": "推荐新手和规模化投放使用"},
            {"name": "Advantage+ 受众", "desc": "v23.0起默认开启，定向设置变为'建议信号'而非硬约束，系统可扩展到建议之外的用户", "recommendation": "除非有强定向需求(如重定向)，建议保持开启"},
            {"name": "Advantage+ 版位", "desc": "全选所有版位让Meta自动分配预算到效果最好的版位", "recommendation": "强烈推荐，比手动选版位效果通常更好"},
            {"name": "Advantage+ 创意", "desc": "v22.0起拆分为独立增强项，可逐个控制image_templates/text_optimization等", "recommendation": "建议开启text_optimizations和image_touchups"},
            {"name": "CBO", "desc": "Campaign级预算优化，系统自动将预算分配给效果最好的Ad Set", "recommendation": "3+个Ad Set时推荐开启"},
        ],
        "important_notes": [
            "v25.0起smart_promotion_type字段废弃，Advantage+状态通过advantage_state_info自动判定",
            "v23.0起advantage_audience默认=1，不设置时会自动开启扩展定向",
            "v22.0起Advantage+创意标准增强包拆分，需逐项设置(90天过渡期)",
            "特殊广告类别(HOUSING/EMPLOYMENT/CREDIT)限制年龄/性别/ZIP定向",
            "Learning Phase: 新Ad Set需约50次优化事件(通常3-5天)才能稳定，期间避免大幅调整",
        ],
    },
    "google": {
        "platform": "Google Ads", "icon": "G", "color": "#4285f4",
        "api_version": "v18 (2024-2025)",
        "last_updated": "2025-06",
        "creation_flow": [
            {"step": 1, "name": "Campaign层", "fields": [
                {"field": "advertising_channel_type", "label": "广告系列类型", "type": "select", "required": True,
                 "options": ["MULTI_CHANNEL (App Campaign)", "PERFORMANCE_MAX", "SEARCH", "DISPLAY", "VIDEO", "DEMAND_GEN"],
                 "note": "App推广最常用MULTI_CHANNEL(UAC)，效果广告推荐PERFORMANCE_MAX"},
                {"field": "advertising_channel_sub_type", "label": "子类型", "type": "select", "required": "App Campaign必选",
                 "options": ["APP_CAMPAIGN (安装)", "APP_CAMPAIGN_FOR_ENGAGEMENT (互动)", "APP_CAMPAIGN_FOR_PRE_REGISTRATION (预注册)"],
                 "note": "APP_CAMPAIGN最常用，优化安装或应用内事件"},
                {"field": "app_campaign_setting.app_id", "label": "应用ID", "type": "text", "required": "App Campaign必填",
                 "note": "格式: Android='com.example.app', iOS='123456789'"},
                {"field": "app_campaign_setting.app_store", "label": "应用商店", "type": "select", "required": True,
                 "options": ["GOOGLE_APP_STORE", "APPLE_APP_STORE"],
                 "note": "与app_id对应"},
                {"field": "app_campaign_setting.bidding_strategy_goal_type", "label": "出价策略目标", "type": "select", "required": True,
                 "options": ["OPTIMIZE_INSTALLS_TARGET_INSTALL_COST (目标CPI优化安装)", "OPTIMIZE_IN_APP_CONVERSIONS_TARGET_INSTALL_COST (优化应用内转化)", "OPTIMIZE_IN_APP_CONVERSIONS_TARGET_CONVERSION_COST (目标CPA)", "OPTIMIZE_RETURN_ON_ADVERTISING_SPEND (目标ROAS)"],
                 "note": "【核心选项】决定Google的机器学习优化方向"},
                {"field": "campaign_budget", "label": "日预算", "type": "number", "required": True,
                 "note": "需单独创建CampaignBudget资源，不支持共享预算。App Campaign建议≥$50/天(≥目标CPI×10)"},
                {"field": "bidding_strategy / target_cpa / target_roas", "label": "出价金额", "type": "number",
                 "note": "MAXIMIZE_CONVERSIONS可设target_cpa; MAXIMIZE_CONVERSION_VALUE可设target_roas; App Campaign通过bidding_strategy_goal_type控制"},
                {"field": "geo_target_type_setting", "label": "地区定向", "type": "multi_select", "required": True,
                 "note": "通过CampaignCriterion添加GeoTarget，使用geo_target_constant资源ID"},
                {"field": "language_setting", "label": "语言定向", "type": "multi_select",
                 "note": "通过CampaignCriterion添加语言"},
                {"field": "network_settings", "label": "网络设置", "type": "multi_toggle",
                 "note": "App Campaign由Google自动分配(Search/Display/YouTube/Play)，不可手动选择"},
                {"field": "start_date / end_date", "label": "排期", "type": "date",
                 "note": "格式YYYY-MM-DD，end_date可选"},
            ]},
            {"step": 2, "name": "Ad Group层", "fields": [
                {"field": "type", "label": "广告组类型", "type": "auto",
                 "note": "App Campaign不需要设type字段，系统自动处理"},
                {"field": "target_cpa_micros", "label": "广告组级CPA", "type": "number", "required": False,
                 "note": "仅APP_CAMPAIGN_FOR_ENGAGEMENT可在Ad Group层覆盖Campaign的CPA出价"},
                {"field": "targeting (Ad Group Criterion)", "label": "定向设置", "type": "auto",
                 "note": "【重要】App Campaign(UAC)不支持手动添加定向，Google完全自动化。ENGAGEMENT类型必须添加user_list_info受众"},
            ]},
            {"step": 3, "name": "Ad / Asset层", "fields": [
                {"field": "ad_group_ad (AppAdInfo)", "label": "App广告", "type": "object", "required": True,
                 "note": "通过AdGroupAdService创建，类型为AppAdInfo/AppEngagementAdInfo/AppPreRegistrationAdInfo"},
                {"field": "headlines", "label": "标题", "type": "text_list", "required": True,
                 "note": "最多5个标题，每个≤30字符，Google自动组合测试"},
                {"field": "descriptions", "label": "描述", "type": "text_list", "required": True,
                 "note": "最多5个描述，每个≤90字符"},
                {"field": "images", "label": "图片素材", "type": "asset_list",
                 "note": "推荐至少3张，尺寸: 1200×628(横版必选)、1200×1200(方形)、480×800(竖版)"},
                {"field": "videos", "label": "视频素材", "type": "asset_list",
                 "note": "YouTube视频ID，推荐3个以上，横版+竖版+方形，时长10-30秒"},
                {"field": "html5_media_bundles", "label": "HTML5素材", "type": "asset_list",
                 "note": "Playable广告，≤1MB，可选"},
            ]},
        ],
        "smart_features": [
            {"name": "App Campaign (UAC)", "desc": "Google最核心的App推广产品，全自动化——只需提供素材+文案+出价+预算，系统自动在Search/Display/YouTube/Play/Discover分配", "recommendation": "App推广首选，不要试图手动控制版位和定向"},
            {"name": "Performance Max", "desc": "跨渠道全自动Campaign，覆盖Search/Display/YouTube/Discover/Gmail/Maps等所有Google渠道", "recommendation": "电商/Lead Gen首选，v21+自动启用Brand Guidelines"},
            {"name": "Smart Bidding", "desc": "Google ML自动出价，支持Target CPA/Target ROAS/Maximize Conversions/Maximize Value", "recommendation": "始终使用Smart Bidding，手动出价效果通常更差"},
            {"name": "Asset Group", "desc": "Performance Max的素材组，提供多种素材让Google自动组合测试", "recommendation": "每个Campaign至少3个Asset Group，覆盖不同受众信号"},
        ],
        "important_notes": [
            "App Campaign(UAC)高度自动化：不支持手动选择版位、关键词、受众定向，全由Google ML控制",
            "Ad Group层在App Campaign中几乎无可配置项(除ENGAGEMENT类型的受众和CPA覆盖)",
            "素材是唯一可控的核心杠杆：标题5个+描述5个+图片3+张+视频3+个，Google自动组合测试",
            "预算建议≥目标CPI×10/天，过低会导致Learning Period过长",
            "Conversion Tracking必须提前配好：Firebase或MMP(AppsFlyer/Adjust) Server-to-Server回传",
            "Performance Max v21+自动启用Brand Guidelines，需在同一请求中创建Campaign和CampaignAsset",
            "GAQL是唯一查询方式：SELECT metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_7_DAYS",
        ],
    },
}


@router.get("/channel-configs")
async def get_channel_configs():
    """获取各渠道详细配置链路"""
    return APIResponse(data=CHANNEL_CONFIGS)


@router.get("/channel-configs/{platform}")
async def get_channel_config(platform: str):
    """获取指定渠道的配置链路"""
    cfg = CHANNEL_CONFIGS.get(platform.lower())
    if not cfg:
        return APIResponse(code=404, message=f"Channel config for '{platform}' not found")
    return APIResponse(data=cfg)


@router.get("/pipeline")
async def get_pipeline():
    return APIResponse(data=PIPELINE)


@router.get("/modules")
async def get_modules():
    return APIResponse(data={
        "modules": MODULES,
        "layers_order": LAYERS_ORDER,
        "layer_colors": LAYER_COLORS,
        "layer_descs": LAYER_DESCS,
        "channel_configs": CHANNEL_CONFIGS,
    })


@router.get("/arch-diagram")
async def get_arch_diagram():
    return APIResponse(data=ARCH_DIAGRAM)


@router.get("/platform-comparison")
async def get_platform_comparison():
    return APIResponse(data=PLATFORM_COMPARISON)
