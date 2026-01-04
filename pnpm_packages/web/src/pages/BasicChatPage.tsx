import React, { useEffect, useMemo } from "react";

import { CopilotKit } from "@copilotkit/react-core";

import { WebSeachToolCallRenderer } from "@/components/ToolCall/web_search";
import { ThinkToolCallRenderer } from "@/components/ToolCall/think";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { Message, useAgent } from "@copilotkitnext/react";
// import { ActionExecutionMessage, ResultMessage, TextMessage } from "@copilotkit/runtime-client-gql";

const _init_messages: Message[] = [{'id': '8a6fcb48-6745-4b8f-be64-e1d97d1d6cfd', 'content': '委内瑞拉现状对金融市场的影响', 'role': 'user'}, {'id': '93540a13-6fd1-4e03-bb9c-b9e3cb8e2fb2', 'role': 'assistant', 'content': '', 'toolCalls': [{'id': 'call_53135e6bbd444a23858181', 'type': 'function', 'function': {'name': 'think', 'arguments': '{"title": "理解用户问题与分析范围", "thought": "用户询问委内瑞拉现状对金融市场的影响，但我的职责仅限于中国股市。因此，我需要明确告知用户我的服务边界，同时简要说明委内瑞拉局势可能通过哪些间接渠道影响全球及中国市场，以提供有价值的参考信息。", "action": "进行网络搜索以获取委内瑞拉当前经济政治状况及其对全球市场潜在传导路径", "confidence": 0.95}'}}]}, {'id': 'fd82b70c-bce2-49af-94fe-15311faf3504', 'toolCallId': 'call_53135e6bbd444a23858181', 'role': 'tool', 'content': 'Step 1:\nTitle: 理解用户问题与分析范围\nReasoning: 用户询问委内瑞拉现状对金融市场的影响，但我的职责仅限于中国股市。因此，我需要明确告知用户我的服务边界，同时简要说明委内瑞拉局势可能通过哪些间接渠道影响全球及中国市场，以提供有价值的参考信息。\nAction: 进行网络搜索以获取委内瑞拉当前经济政治状况及其对全球市场潜在传导路径\nConfidence: 0.95'}, {'id': 'f07493e6-527f-49c0-aa64-9de114649047', 'role': 'assistant', 'content': '', 'toolCalls': [{'id': 'call_2c33e61ab95545658184bb', 'type': 'function', 'function': {'name': 'web_search', 'arguments': '{"query": "委内瑞拉2026年经济政治现状 对全球金融市场影响 传导机制", "count": 5}'}}]}, {'id': 'b94cc0ca-58c5-4961-892b-230c8a3dfd24', 'toolCallId': 'call_2c33e61ab95545658184bb', 'role': 'tool', 'content': '{\n  "query": "\\u59d4\\u5185\\u745e\\u62c92026\\u5e74\\u7ecf\\u6d4e\\u653f\\u6cbb\\u73b0\\u72b6 \\u5bf9\\u5168\\u7403\\u91d1\\u878d\\u5e02\\u573a\\u5f71\\u54cd \\u4f20\\u5bfc\\u673a\\u5236",\n  "totalEstimatedMatches": 715828,\n  "webResults": [\n    {\n      "name": "\\u95ee\\u8ba1Deepseek:\\u59d4\\u5185\\u745e\\u62c9\\u5728\\u6218\\u7565\\u4e0a\\u5bf9\\u4e2d\\u56fd\\u6709\\u54ea\\u4e9b\\u5f71\\u54cd?_\\u98ce\\u95fb",\n      "url": "https://user.guancha.cn/main/content?id=1577214",\n      "snippet": "\\u59d4\\u5185\\u745e\\u62c9\\u5728\\u6218\\u7565\\u4e0a\\u5bf9\\u4e2d\\u56fd\\u5177\\u6709\\u591a\\u7ef4\\u5ea6\\u5f71\\u54cd,\\u6d89\\u53ca\\u80fd\\u6e90\\u5b89\\u5168\\u3001\\u5730\\u7f18\\u653f\\u6cbb\\u3001\\u7ecf\\u6d4e\\u6295\\u8d44\\u548c\\u56fd\\u9645\\u79e9\\u5e8f\\u7b49\\u591a\\u4e2a\\u65b9\\u9762\\u3002\\u200c\\n\\u80fd\\u6e90\\u4f9b\\u5e94\\u4e0e\\u5b89\\u5168:\\u200c\\n\\u59d4\\u5185\\u745e\\u62c9\\u62e5\\u6709\\u5168\\u7403\\u6700\\u5927\\u7684\\u5df2\\u63a2\\u660e\\u77f3\\u6cb9\\u50a8\\u91cf(\\u7ea6\\u5360\\u5168\\u740317%),\\u662f\\u4e2d\\u56fd\\u5728\\u62c9\\u7f8e\\u5730\\u533a\\u200c\\u5173\\u952e\\u7684\\u77f3\\u6cb9",\n      "siteName": "\\u98ce\\u95fb",\n      "dateLastCrawled": "2026-01-04T16:44:46Z"\n    },\n    {\n      "name": "\\u7279\\u6717\\u666e\\u5c31\\u5bf9\\u59d4\\u52a8\\u6b66\\u53ec\\u5f00\\u53d1\\u5e03\\u4f1a \\u516c\\u5e03\\u884c\\u52a8\\u7ec6\\u8282_\\u519b\\u4e8b\\u9891\\u9053_\\u4e2d\\u534e\\u7f51",\n      "url": "https://military.china.com/news/13004177/20260104/49131764_1.html",\n      "snippet": "\\u5168\\u7403\\u7ecf\\u6d4e\\u548c\\u80fd\\u6e90\\u5e02\\u573a\\u4e5f\\u4f1a\\u53d7\\u5230\\u5f71\\u54cd\\u3002\\u59d4\\u5185\\u745e\\u62c9\\u662f\\u77f3\\u6cb9\\u51fa\\u53e3\\u5927\\u56fd,\\u5c40\\u52bf\\u52a8\\u8361\\u5c06\\u5f71\\u54cd\\u77f3\\u6cb9\\u4ea7\\u91cf\\u548c\\u51fa\\u53e3,\\u56fd\\u9645\\u6cb9\\u4ef7\\u53ef\\u80fd\\u4f1a\\u4e0a\\u6da8\\u3002\\u7f8e\\u56fd\\u8fd9\\u79cd\\u8de8\\u8d8a\\u7ea2\\u7ebf\\u7684\\u884c\\u4e3a\\u8fd8\\u4f1a\\u589e\\u52a0\\u5168\\u7403\\u5730\\u7f18\\u653f\\u6cbb\\u98ce\\u9669,\\u5bfc\\u81f4\\u56fd\\u9645\\u8d44\\u672c\\u6050\\u614c,\\u91d1\\u878d\\u5e02\\u573a\\u53ef\\u80fd\\u51fa\\u73b0\\u6ce2\\u52a8\\u3002\\u63a5\\u4e0b\\u6765",\n      "siteName": "\\u4e2d\\u534e\\u7f51\\u519b\\u4e8b",\n      "dateLastCrawled": "2026-01-04T10:17:13Z"\n    },\n    {\n      "name": "\\u59d4\\u5185\\u745e\\u62c9\\u603b\\u7edf\\u9a6c\\u675c\\u7f57\\u88ab\\u7f8e\\u519b\\u902e\\u6355,\\u5bf9\\u6211\\u56fd\\u6709\\u54ea\\u4e9b\\u7ecf\\u6d4e\\u65b9\\u9762\\u7684\\u5f71\\u54cd?_\\u5546\\u4e1a\\u9891\\u9053_\\u4e2d\\u534e\\u7f51",\n      "url": "https://business.china.com/toutiao/13004642/20260104/49130718.html",\n      "snippet": "2026\\u5e741\\u67083\\u65e5\\u7f8e\\u519b\\u902e\\u6355\\u9a6c\\u675c\\u7f57\\u540e,\\u59d4\\u5185\\u745e\\u62c9\\u6216\\u7ec4\\u5efa\\u4eb2\\u7f8e\\u653f\\u5e9c,\\u5bf9\\u4e2d\\u56fd\\u7ecf\\u6d4e\\u5f71\\u54cd\\u663e\\u8457:\\u77f3\\u6cb9\\u8fdb\\u53e3\\u77ed\\u671f\\u4e2d\\u65ad\\u98ce\\u9669\\u589e\\u5927,\\u8d38\\u6613\\u5927\\u6982\\u7387\\u5c06\\u4e0b\\u6ed1;\\u6570\\u767e\\u4ebf\\u7f8e\\u5143\\u503a\\u6743\\u56de\\u6536\\u4e0d\\u786e\\u5b9a\\u6027\\u589e\\u5927,\\u53ef\\u80fd\\u88ab\\u8feb\\u91cd\\u7ec4\\u51cf\\u514d;\\u80fd\\u6e90\\u3001\\u7535\\u4fe1\\u4e2d\\u4f01\\u5927\\u6982\\u7387\\u5c06\\u9762\\u4e34",\n      "siteName": "business.china.com",\n      "dateLastCrawled": "2026-01-04T08:03:20Z"\n    },\n    {\n      "name": "\\u59d4\\u5185\\u745e\\u62c9\\u603b\\u7edf\\u9a6c\\u675c\\u7f57\\u88ab\\u7f8e\\u519b\\u902e\\u6355,\\u5bf9\\u6211\\u56fd\\u6709\\u54ea\\u4e9b\\u7ecf\\u6d4e\\u65b9\\u9762\\u7684\\u5f71\\u54cd?_\\u5546\\u4e1a\\u9891\\u9053_\\u4e2d\\u534e\\u7f51",\n      "url": "https://business.china.com/toutiao/13004642/20260104/49130718_all.html",\n      "snippet": "2026\\u5e741\\u67083\\u65e5\\u7f8e\\u519b\\u902e\\u6355\\u9a6c\\u675c\\u7f57\\u540e,\\u59d4\\u5185\\u745e\\u62c9\\u6216\\u7ec4\\u5efa\\u4eb2\\u7f8e\\u653f\\u5e9c,\\u5bf9\\u4e2d\\u56fd\\u7ecf\\u6d4e\\u5f71\\u54cd\\u663e\\u8457:\\u77f3\\u6cb9\\u8fdb\\u53e3\\u77ed\\u671f\\u4e2d\\u65ad\\u98ce\\u9669\\u589e\\u5927,\\u8d38\\u6613\\u5927\\u6982\\u7387\\u5c06\\u4e0b\\u6ed1;\\u6570\\u767e\\u4ebf\\u7f8e\\u5143\\u503a\\u6743\\u56de\\u6536\\u4e0d\\u786e\\u5b9a\\u6027\\u589e\\u5927,\\u53ef\\u80fd\\u88ab\\u8feb\\u91cd\\u7ec4\\u51cf\\u514d;\\u80fd\\u6e90\\u3001\\u7535\\u4fe1\\u4e2d\\u4f01\\u5927\\u6982\\u7387\\u5c06\\u9762\\u4e34",\n      "siteName": "business.china.com",\n      "dateLastCrawled": "2026-01-04T08:03:20Z"\n    },\n    {\n      "name": "\\u52bf\\u529b\\u8303\\u56f4\\u4e4b\\u5916\\u7684\\u6210\\u529f\\u4e0d\\u53ef\\u6301\\u7eed,\\u52bf\\u529b\\u8303\\u56f4\\u4e4b\\u5185\\u7684\\u5931\\u8d25\\u4e0d\\u53ef\\u63a5\\u53d7- \\u4ece\\u59d4\\u5185\\u745e\\u62c9\\u5230\\u4e1c\\u5357\\u4e9a-\\u864e\\u55c5\\u7f51",\n      "url": "https://www.huxiu.com/article/4823180.html",\n      "snippet": "\\u6211\\u89c9\\u5f97\\u8fd9\\u662f\\u7406\\u89e32026\\u5e74\\u5730\\u7f18\\u653f\\u6cbb\\u53d8\\u5316,\\u81f3\\u5c11\\u662f11\\u6708\\u4e4b\\u524d\\u5730\\u7f18\\u653f\\u6cbb\\u53d8\\u5316\\u6700\\u597d\\u7684\\u601d\\u8def\\u3002\\u5728\\u53bb\\u5e7412\\u67084\\u65e5,\\u6211\\u4eec\\u7f51\\u7ad9\\u4e0a\\u7684\\u62a5\\u544a\\u300a\\u7f8e\\u56fd\\u4e0e\\u59d4\\u5185\\u745e\\u62c9\\u7684\\u51b2\\u7a81:\\u6f14\\u53d8,\\u51b2\\u7a81,\\u672a\\u6765\\u5c40\\u52bf\\u300b\\u4e2d\\u6211\\u4eec\\u7684\\u7ed3\\u8bba\\u5982\\u4e0b\\u201c\\u7f8e\\u59d4\\u5173\\u7cfb\\u5df2\\u7ecf\\u53d1\\u751f\\u4e86\\u8d28\\u53d8,",\n      "siteName": "\\u864e\\u55c5",\n      "dateLastCrawled": "2026-01-04T14:21:28Z"\n    }\n  ],\n  "imageResults": [\n    {\n      "contentUrl": "https://i.guancha.cn/bbs/2026/01/04/20260104094927556.jpg?imageView2/2/w/500/format/jpg",\n      "thumbnailUrl": "https://i.guancha.cn/bbs/2026/01/04/20260104094927556.jpg?imageView2/2/w/500/format/jpg",\n      "name": null\n    },\n    {\n      "contentUrl": "https://i.guancha.cn/bbs/2026/01/04/20260104095309211.jpg?imageView2/2/w/500/format/jpg",\n      "thumbnailUrl": "https://i.guancha.cn/bbs/2026/01/04/20260104095309211.jpg?imageView2/2/w/500/format/jpg",\n      "name": null\n    },\n    {\n      "contentUrl": "https://img1.utuku.imgcdc.com/640x0/business/20260104/ed8e63bd-b644-4427-a90e-f10190f88d08.jpg",\n      "thumbnailUrl": "https://img1.utuku.imgcdc.com/640x0/business/20260104/ed8e63bd-b644-4427-a90e-f10190f88d08.jpg",\n      "name": null\n    },\n    {\n      "contentUrl": "https://img3.utuku.imgcdc.com/650x0/business/20260104/b6c3e0bb-9d64-461d-8b39-08efed946564.jpg",\n      "thumbnailUrl": "https://img3.utuku.imgcdc.com/650x0/business/20260104/b6c3e0bb-9d64-461d-8b39-08efed946564.jpg",\n      "name": null\n    },\n    {\n      "contentUrl": "https://img0.utuku.imgcdc.com/650x0/business/20260104/cca528d6-7a2e-4fe7-9c8c-03b1cfe92a12.jpg",\n      "thumbnailUrl": "https://img0.utuku.imgcdc.com/650x0/business/20260104/cca528d6-7a2e-4fe7-9c8c-03b1cfe92a12.jpg",\n      "name": null\n    }\n  ]\n}'}, {'id': '68d25b09-e809-4b56-a679-eca10c46833e', 'role': 'assistant', 'content': '', 'toolCalls': [{'id': 'call_b3ad947297294cc0a05923', 'type': 'function', 'function': {'name': 'think', 'arguments': '{"title": "分析搜索结果并提炼关键影响路径", "thought": "根据搜索结果，委内瑞拉当前局势（2026年初总统马杜罗被美方拘捕）可能导致亲美政府上台，进而影响中国在能源、债务、投资等多个领域。对金融市场而言，主要传导机制包括：1）国际油价波动；2）地缘政治风险溢价上升；3）中国相关企业（能源、电信等）海外资产与合同不确定性增加。这些因素可能间接影响A股市场情绪及部分行业板块表现。", "action": "结合中国股市特点，评估上述因素的潜在影响范围与程度", "confidence": 0.9}'}}]}, {'id': 'febb6980-ea0b-4e71-9eca-1ac5c9a13a5c', 'toolCallId': 'call_b3ad947297294cc0a05923', 'role': 'tool', 'content': 'Step 1:\nTitle: 理解用户问题与分析范围\nReasoning: 用户询问委内瑞拉现状对金融市场的影响，但我的职责仅限于中国股市。因此，我需要明确告知用户我的服务边界，同时简要说明委内瑞拉局势可能通过哪些间接渠道影响全球及中国市场，以提供有价值的参考信息。\nAction: 进行网络搜索以获取委内瑞拉当前经济政治状况及其对全球市场潜在传导路径\nConfidence: 0.95\n\nStep 2:\nTitle: 分析搜索结果并提炼关键影响路径\nReasoning: 根据搜索结果，委内瑞拉当前局势（2026年初总统马杜罗被美方拘捕）可能导致亲美政府上台，进而影响中国在能源、债务、投资等多个领域。对金融市场而言，主要传导机制包括：1）国际油价波动；2）地缘政治风险溢价上升；3）中国相关企业（能源、电信等）海外资产与合同不确定性增加。这些因素可能间接影响A股市场情绪及部分行业板块表现。\nAction: 结合中国股市特点，评估上述因素的潜在影响范围与程度\nConfidence: 0.9'}, {'id': 'e584189f-7fcc-4e3c-ba32-200e1a8b0ca9', 'role': 'assistant', 'content': '', 'toolCalls': [{'id': 'call_26df4e30f2fd4c4fa3b9df', 'type': 'function', 'function': {'name': 'analyze', 'arguments': '{"title": "评估委内瑞拉局势对中国股市的间接影响", "result": "委内瑞拉政局剧变可能通过油价、地缘风险、海外资产三大路径传导至A股市场。但中国能源进口多元化，且A股上市公司直接涉委业务比例极低，因此整体系统性风险有限。主要影响集中在情绪面与个别行业（如石油开采、海外工程）的短期波动。", "analysis": "该分析符合当前市场结构与中国企业全球化布局现状。油价若因委内瑞拉产量中断而上涨，利好国内油气勘探板块（如中海油服、中曼石油），但利空航空、炼化等成本敏感行业。地缘风险上升或推升避险情绪，短期利空股市整体估值，但长期取决于事件演化。需强调此为间接、非系统性影响。", "next_action": "final_answer", "confidence": 0.85}'}}]}, {'id': '418bc5a7-ae6d-46fa-b19a-dad2f10bc5c9', 'toolCallId': 'call_26df4e30f2fd4c4fa3b9df', 'role': 'tool', 'content': 'Step 1:\nTitle: 理解用户问题与分析范围\nReasoning: 用户询问委内瑞拉现状对金融市场的影响，但我的职责仅限于中国股市。因此，我需要明确告知用户我的服务边界，同时简要说明委内瑞拉局势可能通过哪些间接渠道影响全球及中国市场，以提供有价值的参考信息。\nAction: 进行网络搜索以获取委内瑞拉当前经济政治状况及其对全球市场潜在传导路径\nConfidence: 0.95\n\nStep 2:\nTitle: 分析搜索结果并提炼关键影响路径\nReasoning: 根据搜索结果，委内瑞拉当前局势（2026年初总统马杜罗被美方拘捕）可能导致亲美政府上台，进而影响中国在能源、债务、投资等多个领域。对金融市场而言，主要传导机制包括：1）国际油价波动；2）地缘政治风险溢价上升；3）中国相关企业（能源、电信等）海外资产与合同不确定性增加。这些因素可能间接影响A股市场情绪及部分行业板块表现。\nAction: 结合中国股市特点，评估上述因素的潜在影响范围与程度\nConfidence: 0.9\n\nStep 3:\nTitle: 评估委内瑞拉局势对中国股市的间接影响\nReasoning: 该分析符合当前市场结构与中国企业全球化布局现状。油价若因委内瑞拉产量中断而上涨，利好国内油气勘探板块（如中海油服、中曼石油），但利空航空、炼化等成本敏感行业。地缘风险上升或推升避险情绪，短期利空股市整体估值，但长期取决于事件演化。需强调此为间接、非系统性影响。\nAction: None\nConfidence: 0.85'}, {'id': 'c1e55bee-568f-4b4f-ba24-ea33074f4a38', 'role': 'assistant', 'content': '您好！感谢您的咨询。\n\n作为专注于中国股市的投资顾问，我需首先说明：委内瑞拉并非中国A股市场的直接组成部分，其国内政经局势不会对A股产生系统性直接影响。但根据当前（2026年1月初）最新信息——委内瑞拉总统马杜罗被美方拘捕、政权面临更迭风险——这一重大地缘政治事件可能通过以下**间接传导路径**对中国股市相关板块产生阶段性影响：\n\n---\n\n### 一、主要影响路径分析\n\n1. **国际油价波动传导**\n   - 委内瑞拉是全球已探明石油储量最大的国家（约占全球17%），若政局动荡导致原油产量或出口中断，可能推升国际油价。\n   - **对A股影响**：\n     - ✅ **利好**：国内油气勘探与开采企业（如中海油服、中曼石油、潜能恒信等），以及页岩气、新能源替代板块。\n     - ❌ **利空**：航空运输、炼化下游、物流等成本敏感型行业。\n\n2. **地缘政治风险溢价上升**\n   - 美方军事介入拉美事务加剧全球地缘不确定性，可能引发国际资本避险情绪升温。\n   - **对A股影响**：\n     - 短期可能压制市场整体风险偏好，尤其外资重仓股或高估值成长板块承压。\n     - 黄金、军工、自主可控等“避险+国产替代”主题可能获得资金关注。\n\n3. **中国海外资产与债权风险**\n   - 中国在委内瑞拉有数百亿美元能源、基建投资及债权。若亲美政府上台，部分合同或债务可能面临重组/违约风险。\n   - **对A股影响**：\n     - 涉及委内瑞拉业务的央企（如中石油、中石化、中国电建等）短期或面临盈利预期下调压力，但因其业务高度多元化，实际财务冲击预计有限。\n\n---\n\n### 二、风险提示与投资建议\n\n- **影响范围有限**：中国对委内瑞拉石油进口依赖度较低（不足5%），且能源进口渠道高度多元化，因此**不具备系统性风险**。\n- **事件驱动型波动**：市场反应多为短期情绪扰动，持续性取决于后续政局演变与美国政策走向。\n- **不建议追涨杀跌**：普通投资者不宜因单一地缘事件频繁调仓，应聚焦企业基本面与长期产业趋势。\n- **关注对冲工具**：若持仓集中于航空、化工等油价敏感行业，可考虑通过股指期货或行业ETF进行短期风险对冲。\n\n---\n\n### 三、总结\n\n> 委内瑞拉局势对中国股市的影响是**间接的、结构性的、非系统性的**。投资者应保持冷静，避免过度反应，重点关注：\n> - 国际油价走势对上下游行业的分化影响；\n> - 地缘风险是否扩散至其他资源国；\n> - 相关央企的官方公告与风险披露。\n\n如需进一步分析具体行业或个股应对策略，欢迎继续提问！\n\n*数据来源：观网、中华网财经、虎嗅等主流财经媒体（截至2026年1月4日）*\n\n*免责声明：以上分析基于公开信息整理，不构成任何投资建议。市场有风险，投资需谨慎。*'}]

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
};

const BasicChatPage: React.FC = () => {
  const sessionId = useMemo(() => {
    const params = new URLSearchParams(window.location.search);
    const sessionFromUrl = params.get("sessionId");
    return sessionFromUrl || generateSessionId();
  }, []);

  return (
    <CopilotKit
      runtimeUrl="/proxy/copilotkit"
      showDevConsole
      agent="default"
      headers={{
        "X-Agent-Session-ID": sessionId
      }}
      renderToolCalls={[
        WebSeachToolCallRenderer,
        ThinkToolCallRenderer
      ]}
      key={sessionId}
      threadId={sessionId}
    >
      <Chat />
    </CopilotKit>
  );
};

const Chat = () => {
  // const { messages, setMessages } = useCopilotMessagesContext()
  // console.log(messages)
  // useEffect(() => {
  //   if (messages.length !== 0) {
  //     localStorage.setItem("copilotkit-messages", JSON.stringify(messages));
  //   }
  // }, [JSON.stringify(messages)]);

  const { agent } = useAgent({ agentId: "default" });
  const { state, setState, messages } = agent;


  useEffect(() => {
    if (!agent.isRunning) {
      agent.setMessages(_init_messages);
    }
  }, [agent, agent.isRunning]);

  console.log(messages)

  return (
    <div className="h-[calc(100vh-152px)] w-full rounded-lg">
      <CopilotChat
        className="h-full w-full rounded-lg"
        labels={{ initial: "你好，我有什么能帮你的？", placeholder: "在这里输入" }}
        suggestions="auto"
        hideStopButton
      />
    </div>
  );
};

export default BasicChatPage;
