import requests

class F10Client:
    def __init__(self):
        self.url = "https://dz-f10.cf69.com/f10/api/"
        self.headers = {
            "Accept-Language": "zh-CN",
            "Org-key": "dz",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    # ---------------------------------------------------------
    # 2005 - 现金流量明细
    # ---------------------------------------------------------
    def get_cashflow_detail(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        order_by_date="asc",
    ):
        """
        mode_code = 2005
        查询现金流量数据
        """


        all_records = []
        page_num = 1
        page_size = 100  # 固定较大值，不需要你自己设定

        while True:
            body = {
                "stk_id": stk_id,
                "fields": fields,
                "order_by_date": order_by_date,
                "page_num": page_num,
                "page_size": page_size
            }

            if max_date:
                body["max_date"] = max_date

            payload = {
                "trade_market": trade_market,
                "mode_code": "2005",
                "body": body
            }

            r = requests.post(self.url, headers=self.headers, json=payload).json()

            # 出错直接退出
            if not r.get("success"):
                print("Error:", r)
                break

            result = r.get("result", {})
            datas = result.get("datas", [])

            # 没数据就停止
            if not datas:
                break

            # 累加数据
            all_records.extend(datas)

            # 判断是否有下一页
            next_page = result.get("netx_page", 0)
            if next_page == 0:
                break

            page_num = next_page   # 自动翻页

        # ------ 全部数据抓取完毕，开始简化格式 -------
        # fields[0] like "ROA" / "ROE" / "EPS"
        simplified = self.simplify_finance_data(
            {"result": {"datas": all_records}},
            fields[0]
        )

        return simplified
    



    # ---------------------------------------------------------
    # 2004 - 资产负债表
    # ---------------------------------------------------------
    def get_balance_sheet(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        order_by_date="asc",
    ):
        """
        mode_code = 2004 资产负债表
        """

        all_records = []
        page_num = 1
        page_size = 100  # 固定较大值，不需要你自己设定

        while True:
            body = {
                "stk_id": stk_id,
                "fields": fields,
                "order_by_date": order_by_date,
                "page_num": page_num,
                "page_size": page_size
            }

            if max_date:
                body["max_date"] = max_date

            payload = {
                "trade_market": trade_market,
                "mode_code": "2004",
                "body": body
            }

            r = requests.post(self.url, headers=self.headers, json=payload).json()

            # 出错直接退出
            if not r.get("success"):
                print("Error:", r)
                break

            result = r.get("result", {})
            datas = result.get("datas", [])

            # 没数据就停止
            if not datas:
                break

            # 累加数据
            all_records.extend(datas)

            # 判断是否有下一页
            next_page = result.get("netx_page", 0)
            if next_page == 0:
                break

            page_num = next_page   # 自动翻页

        # ------ 全部数据抓取完毕，开始简化格式 -------

        simplified = self.simplify_finance_data(
            {"result": {"datas": all_records}},
            fields[0]
        )

        return simplified




    # ---------------------------------------------------------
    # 2002 -  财务比率
    # ---------------------------------------------------------

    def get_financial_ratios(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        order_by_date="asc",
    ):
        """
        自动获取所有 ROA / ROE / EPS / 等财务比率（无需指定 page_size）
        mode_code = 2002
        """

        all_records = []
        page_num = 1
        page_size = 100  # 固定较大值，不需要你自己设定

        while True:
            body = {
                "stk_id": stk_id,
                "fields": fields,
                "order_by_date": order_by_date,
                "page_num": page_num,
                "page_size": page_size
            }

            if max_date:
                body["max_date"] = max_date

            payload = {
                "trade_market": trade_market,
                "mode_code": "2002",
                "body": body
            }

            r = requests.post(self.url, headers=self.headers, json=payload).json()

            # 出错直接退出
            if not r.get("success"):
                print("Error:", r)
                break

            result = r.get("result", {})
            datas = result.get("datas", [])

            # 没数据就停止
            if not datas:
                break

            # 累加数据
            all_records.extend(datas)

            # 判断是否有下一页
            next_page = result.get("netx_page", 0)
            if next_page == 0:
                break

            page_num = next_page   # 自动翻页

        # ------ 全部数据抓取完毕，开始简化格式 -------

        simplified = self.simplify_finance_data(
            {"result": {"datas": all_records}},
            fields[0]
        )

        return simplified






    # ---------------------------------------------------------
    # 2003 -  利润表 
    # ---------------------------------------------------------
 
    def get_income(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        order_by_date="asc",
    ):

        all_records = []
        page_num = 1
        page_size = 100  # 固定较大值，不需要你自己设定

        while True:
            body = {
                "stk_id": stk_id,
                "fields": fields,
                "order_by_date": order_by_date,
                "page_num": page_num,
                "page_size": page_size
            }

            if max_date:
                body["max_date"] = max_date

            payload = {
                "trade_market": trade_market,
                "mode_code": "2003",
                "body": body
            }

            r = requests.post(self.url, headers=self.headers, json=payload).json()

            # 出错直接退出
            if not r.get("success"):
                print("Error:", r)
                break

            result = r.get("result", {})
            datas = result.get("datas", [])

            # 没数据就停止
            if not datas:
                break

            # 累加数据
            all_records.extend(datas)

            # 判断是否有下一页
            next_page = result.get("netx_page", 0)
            if next_page == 0:
                break

            page_num = next_page   # 自动翻页

        # ------ 全部数据抓取完毕，开始简化格式 -------

        simplified = self.simplify_finance_data(
            {"result": {"datas": all_records}},
            fields[0]
        )

        return simplified

   

    # ---------------------------------------------------------
    # 1010 -  股东 
    # ---------------------------------------------------------
    def get_stock(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        order_by_date="asc",
    ):

        all_records = []
        page_num = 1
        page_size = 100  # 固定较大值，不需要你自己设定

        while True:
            body = {
                "stk_id": stk_id,
                "fields": fields,
                "order_by_date": order_by_date,
                "page_num": page_num,
                "page_size": page_size
            }

            if max_date:
                body["max_date"] = max_date

            payload = {
                "trade_market": trade_market,
                "mode_code": "1010",
                "body": body
            }

            r = requests.post(self.url, headers=self.headers, json=payload).json()

            # 出错直接退出
            if not r.get("success"):
                print("Error:", r)
                break

            result = r.get("result", {})
            datas = result.get("datas", [])

            # 没数据就停止
            if not datas:
                break

            # 累加数据
            all_records.extend(datas)

            # 判断是否有下一页
            next_page = result.get("netx_page", 0)
            if next_page == 0:
                break

            page_num = next_page   # 自动翻页

        # ------ 全部数据抓取完毕，开始简化格式 -------

        simplified = self.simplify_finance_data(
            {"result": {"datas": all_records}},
            fields[0]
        )

        return simplified


    # ---------------------------------------------------------
    # 1001 -  公司概况 
    # ---------------------------------------------------------
    def get_company(
        self,
        stk_id: str,
        fields: list,
        trade_market="SHMK",
        max_date=None,
        page_num=1,
        page_size=20,
      
        ):

        body = {
            "stk_id": stk_id,
            "fields": fields,
            "page_num": page_num,
            "page_size": page_size,
        }

        if max_date:
            body["max_date"] = max_date
        payload = {
            "trade_market": trade_market,
            "mode_code": "1001",
            "body": body
        }

        r = requests.post(self.url, headers=self.headers, json=payload)
        return r.json()
    





    def simplify_finance_data(self, raw_data, value_field):
        result = raw_data.get("result", {}).get("datas", [])
        simplified = {}
        for item in result:
            end_date = item.get("end_date")
            value = item.get(value_field)
            if end_date is not None and value is not None:
                simplified[end_date] = value
        return simplified

client = F10Client()

#资产查阅
# data = client.get_cashflow_detail(
#     stk_id="689009",
#     fields=["cs_10000"],   # 经营流入、流出、净额
#     max_date= "2020-01-01",
#     page_num=1,
#     page_size=50
# )
# print("资产查阅 ")
# print(data)

# fields = [
#     "END_DATE", "INFO_PUB_DATE", "BS_11001", "BS_1100101", "BS_11004",
#     "BS_1100401", "BS_11007", "BS_11010", "BS_11013", "BS_11016",
#     "BS_11019", "BS_11022", "BS_11025", "BS_11028", "BS_11029",
#     "BS_11031", "BS_11002", "BS_11017", "BS_11018", "BS_11034",
#     "BS_11037", "BS_11067", "BS_11043", "BS_11046", "BS_11049",
#     "BS_11052", "BS_11055", "BS_11058", "BS_11061", "BS_11064",
#     "BS_11070", "BS_11003", "BS_1107301", "BS_11026", "BS_11027",
#     "BS_11076", "BS_11079", "BS_11082", "BS_CASPEC", "BS_11000",
#     "BS_12002", "BS_12004", "BS_12007", "BS_12010", "BS_12003",
#     "BS_12005", "BS_12013", "BS_12016", "BS_12019", "BS_12022",
#     "BS_12011", "BS_12012", "BS_12025", "BS_12001", "BS_12037",
#     "BS_12034", "BS_12031", "BS_12040", "BS_12043", "BS_12032",
#     "BS_12046", "BS_1204601", "BS_12049", "BS_12052", "BS_12055",
#     "BS_12058", "BS_12061", "BS_12064", "BS_12067", "BS_12000",
#     "BS_10000", "BS_21003", "BS_2100101", "BS_21004", "BS_21007",
#     "BS_21010", "BS_21013", "BS_21016", "BS_21019", "BS_21022",
#     "BS_21025", "BS_21028", "BS_21031", "BS_21034", "BS_21037",
#     "BS_21040", "BS_21043", "BS_21046", "BS_21049", "BS_21052",
#     "BS_21055", "BS_21058", "BS_21061", "BS_21064", "BS_21067",
#     "BS_21068", "BS_21070", "BS_21001", "BS_21002", "BS_21017",
#     "BS_21079", "BS_21026", "BS_21082", "BS_21088", "BS_21091",
#     "BS_21032", "BS_21085", "BS_21094", "BS_21097", "BS_21100",
#     "BS_21000", "BS_22001", "BS_22004", "BS_22005", "BS_22007",
#     "BS_22010", "BS_22013", "BS_22016", "BS_22019", "BS_22017",
#     "BS_22022", "BS_22025", "BS_22000", "BS_20000", "BS_30001",
#     "BS_30002", "BS_31007", "BS_30005", "BS_30006", "BS_30003",
#     "BS_31037", "BS_30004", "BS_31022", "BS_31025", "BS_31000",
#     "BS_32000", "BS_30000", "BS_40000"
# ]


#负债查阅
# data = client.get_balance_sheet(
#     stk_id="688777",
#     fields=["BS_11003"],
#     #fields=["BS_11029","BS_11003","BS_21000"],
#     #fields=["BS_21000"],
#     #fields=fields,
#     max_date="2020-01-01",
#     order_by_date="asc",
#     page_num=1,
#     page_size=100
# )
# print("负债查阅 ")
# print(data)


# ratios_fields = [
#     "END_DATE", "INFO_PUB_DATE", "BEPS", "DEPS", "EPSED", "EPSNED",
#     "BEPS_DED", "DEPS_DED", "EPSED_DED", "EPS_MOV", "EPS_TTM",
#     "BPS", "BPSNED", "PS_OCF", "PER_OFW_TTM", "PS_TOR",
#     "PS_OR", "PER_OPR_TTM", "PS_CR", "PS_SR", "PS_UP", "PS_RE",
#     "PS_CN", "PER_CFW_TTM", "PS_EBIT", "PS_DIV", "ROEA", "ROEW",
#     "ROED", "ROEA_DED", "ROEW_DED", "ROED_DED", "ROE_AIC",
#     "FFD_ROE_12M", "FFD_ROEAPC_12M", "ROA", "ROA_NP", "ROIC",
#     "ROE_YEAR", "ROA_YEAR", "ROA_NYEAR", "SAL_NPR", "SAL_GIR",
#     "SAL_COST", "SAL_PFR", "TR_NP", "TR_OP", "TR_EBIT", "TR_TC",
#     "TR_OF", "TR_MF", "TR_FF", "TR_AL", "ROE_PAR", "OP_ASS_RATIO",
#     "OP_EQT_RATIO", "NON_RECR_FREQ", "SUSTAINABLE_GR", "DVD_COVER",
#     "DVD_PAID_RATIO", "RET_EARN_RATIO", "CASH_DVD_COV",
#     "HOLD_EQT_YOY", "TP_ONI", "TP_VCI", "TP_NON", "TP_TAX",
#     "OR_SAL", "OR_OCF", "OR_ONI", "FCFF", "NET_CASH_FLOW",
#     "CPT_REVN_RATIO", "ASS_DEBT", "EM", "TA_CA", "TA_NCA",
#     "TA_TA", "TC_PCE", "TC_IBD", "TL_CL", "TL_NCL", "CR", "QR",
#     "KQR", "ER", "TL_PCE", "IBD_PCE", "TL_TA", "IBD_TA", "ND_TA",
#     "TL_OCF", "IBD_OCF", "CL_OCF", "ND_OCF", "IF_EBIT", "WK_LD",
#     "OPE_CYC", "INV_DAYS", "ARC_DAYS", "INV_RATE", "ARC_RATE",
#     "CA_RATE", "FA_RATE", "TA_RATE", "AP_RATE", "AP_DAYS",
#     "EQT_TURN_RATIO", "BEPS_YOY", "DEPS_YOY", "PS_OCF_YOY", "TR_YOY",
#     "OR_YOY", "OP_YOY", "TP_YOY", "PCNP_YOY", "PCNDP_YOY",
#     "OCF_YOY", "ROE_YOY", "NP_YOY", "NET_CASH_FLOW_GR",
#     "OP_PROFIT_GR", "FIN_NP_12MG", "FIN_OR_12MG",
#     "FIN_OCE_12MG", "FIN_TOE_G", "BPS_YTD", "TA_YTD", "PCE_YTD",
#     "EARNING_CHG", "CASH_FLOW_CHG_GR", "INC_A", "INC_B", "INC_C",
#     "INC_D", "INC_E", "INC_F", "LOG_TOT_OP_REVENUE",
#     "NET_NON_OP_INCOME", "NP_TP_RATIO", "NP_CUT_NP_RATIO",
#     "NP_TTM_OR_RATIO", "NP_REVN_RATIO", "NP_CUT_REVN_RATIO",
#     "EXTR_NP_RATIO", "GP_REVN_RATIO", "BAL_A", "BAL_B", "BAL_C",
#     "BAL_D", "BAL_E", "BAL_F", "BAL_G", "BAL_H", "BAL_I",
#     "TOT_ASS_LN", "RECV_PAY_RATIO", "CURT_DEBT_RATIO",
#     "EQT_ASS_RATIO", "ITGB_ASS_RATIO", "DR", "OC_DEBT_RATIO",
#     "OPER_CASH_ASS_RATIO"
# ]

#查看比率
# data = client.get_financial_ratios(
#     stk_id="688777",
#     #fields=["ROA"],
#     fields=["ROA"],
#     #fields=ratios_fields,
#     max_date="2024-01-01",
#     order_by_date="asc",
# )
# print(data)

# #利润查看
# data = client.get_income(
#     stk_id="600000",
#     fields=["IS_50000","IS_10000"],
#     #fields=ratios_fields,
#     max_date="2024-01-01",
#     order_by_date="asc",
#     page_num=1,
#     page_size=50
# )
# print(data)

# #股份查看
# data = client.get_stock(
#     stk_id="600000",
#     fields=["HOLD_SHR_PROP"],
#     #fields=ratios_fields,
    

#     page_num=1,
#     page_size=50,
#     holder_type=1
# )
# print(data)


# #公司查看
data = client. get_company(
    stk_id="600000",
    fields=["man_staff_num"],
    #fields=ratios_fields,
    page_num=1,
    page_size=50,
 
)
print(data)